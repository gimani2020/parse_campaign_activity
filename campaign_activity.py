import zipfile
import gzip
import os
import shutil
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--zipfile', nargs='?', const=1, default='raw_data_fiels.zip')
parser.add_argument('--dim', nargs='?', const=1, default='Consumer_DimCampaign_Daily_FULL_20170707.txt.gz')
args = parser.parse_args()


working_dir = '/tmp/harman_task/'
zip_file = args.zipfile
extract_folder = '{}mytest'.format(working_dir)
raw_data_folder = '{}/raw_data/'.format(extract_folder)
result_dir = '{}results/'.format(working_dir)
dim_file = args.dim
activity_files_dict = {'UserCenterNewsletterClicksActivity': [], 'UserMediaAllActivity': [], 'UserTrafficCenterActivity': []}


# unzip raw data file.  Raise Exception if dim file not exist
def unzip_file():
    if not os.path.isdir(working_dir):
        os.mkdir(working_dir, 777)
    if not os.path.isfile(working_dir + zip_file):
        shutil.copyfile(zip_file, working_dir + zip_file)
    if not os.path.isdir(extract_folder):
        os.mkdir(extract_folder, 777)
    if os.path.isdir(raw_data_folder):
        shutil.rmtree(raw_data_folder)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
    if not os.path.isfile(raw_data_folder + dim_file):
        raise Exception('dim file : {} ,  not found in the extracted folder '.format(dim_file))


# convert anf format the first line (header) to list
def head_to_list(filename):
    os.chdir(raw_data_folder)
    f = gzip.open(filename, 'rt')
    # assuming all head look the sane (with different columns)
    head = next(f).partition('"')[2].replace('"', '').rstrip().split('|')
    f.close()
    return head


# convert lines to list and return list of lists  (without header & footer lines)
def rows_to_list(filename):
    os.chdir(raw_data_folder)
    f = gzip.open(filename, 'rt')
    next(f)
    list_of_lines = []
    for line in f:
        stripped_line = line.replace('"', '').rstrip().split("|")
        list_of_lines.append(stripped_line)
    rows = list_of_lines[:-1]
    f.close()
    return rows


# activity files arranged in a dict
def activity_files():
    for k, v in activity_files_dict.items():
        for file_name in os.listdir(raw_data_folder):
            if k in file_name:
                v.append(file_name)


# return lines that match "CampaignID", filtered by activity type
def get_activity_for_campaign(campaign_id, activity):
    campaign_activity = []
    files = activity_files_dict[activity]
    for file in files:
        # print('searching file {}'.format(file))
        campaign_id_inx = head_to_list(file).index('CampaignID')
        for line in rows_to_list(file):
            # print(line, campaign_id_inx, line[campaign_id_inx], campaign_id)
            if campaign_id == line[campaign_id_inx]:
                # print(line, campaign_id_inx)
                campaign_activity.append(line)
    return campaign_activity


# return org lines as str (+double quotes, +pipe separator)
def return_org_line_from_list(line):
    q_line = (','.join(map(lambda x: '"' + x + '"', line))).split(",")
    r_line = ''.join([x + '|' for x in q_line])[:-1]
    return r_line


def main():
    # unzip raw data file
    unzip_file()

    # rearrange activity files in a dict
    activity_files()

    # create result folder
    if os.path.isdir(result_dir):
        shutil.rmtree(result_dir)
    os.mkdir(result_dir, 777)
    os.chdir(result_dir)

    # get active campaign
    active_campaign = []
    active_inx = head_to_list(dim_file).index('isActiveFlag')
    id_inx = head_to_list(dim_file).index('CampaignID')
    for line in rows_to_list(dim_file):
        if line[active_inx] == 'Y':
            active_campaign.append(line[id_inx])

    # create activity files for each folder
    for camp in active_campaign:
        if not os.path.isdir(result_dir + camp):
            os.mkdir(result_dir + camp, 777)
        for k, v in activity_files_dict.items():
            head = head_to_list(v[0])
            headache = return_org_line_from_list(head)
            raws = get_activity_for_campaign(camp, k)
            os.chdir(result_dir + camp)
            with gzip.open(k + '.txt.gz', 'wb') as f:
                f.write(headache.encode())
                for line in raws:
                    f.write('\n'.encode())
                    f_line = return_org_line_from_list(line)
                    f.write(f_line.encode())
                f.close()


if __name__ == '__main__':
    main()


