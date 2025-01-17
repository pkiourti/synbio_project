import sys

import numpy as np
import os

bases = 4

project_root = os.environ.get('PYTHONPATH')
try:
    project_root = project_root.split(os.path.pathsep)[1]
except Exception as e:
    pass

def get_saved_models():
    """
    :return: a python list of all saved models. By convention all models are saved under models/.
    """
    return os.listdir(os.path.join(project_root, 'models'))


def delete_model(file_to_remove):
    """
    :args name: a string indicating which model to delete
    :return:
    """
    try:
        os.remove(file_to_remove)
        return True, None
    except Exception as e:
        print(f'File is not deleted. {e}')
        return False, e


def data_files(data_dir_filepath):
    i = 1
    while os.path.exists(os.path.join(data_dir_filepath, 'x_forward_' + str(i) + '.npy')):
        i += 1

    if not os.path.exists(data_dir_filepath):
        os.makedirs(data_dir_filepath)

    return (os.path.join(data_dir_filepath, 'x_forward_' + str(i)),
            os.path.join(data_dir_filepath, 'x_reverse_' + str(i)),
            os.path.join(data_dir_filepath, 'y_' + str(i)))


def rename(new_name, old_name):
    try:
        os.rename(old_name, new_name)
        return True, None
    except Exception as e:
        print(f'File not renamed. {e}')
        return False, e


def switch(argument):
    switcher = {
        "A": 0,
        "T": 1,
        "C": 2,
        "G": 3,
    }
    return switcher.get(argument, "Invalid base")


def complement_base(idx):
    if idx == 0:
        return 1
    elif idx == 1:
        return 0
    elif idx == 2:
        return 3
    elif idx == 3:
        return 2


def convert_dna_seq_to_matrix(dna_seq):
    '''
    Converts single dna_seq input string of integers values 0-3 representing the bases to matrix representation.
        0 = A
        1 = T
        2 = C
        3 = G
    Returns numpy array of dimension bases x len(dna_seq)
    '''
    seq_matrix = np.zeros((4, len(dna_seq)))

    for i in range(len(dna_seq)):
        seq_matrix[dna_seq[i]][i] = 1

    return seq_matrix


# saves data from .txt file to .npy file in /data
# appropriate shape is # samples x 4 x 300 ?
def convert_txt_to_npy(txt_filepath, test=False):
    forward_file, reverse_file, bind_v_file = data_files(os.path.join(project_root, 'data'))

    file = open(txt_filepath, "r")

    dna_seq = []

    if not test:
        binding_vals = []

        i = 1
        for line in file:
            if (i % 2 == 0):  # i.e. every 2nd row contains the binding values
                binding_vals.append(float(line.rstrip()))
            else:
                one_dna_seq = [switch(j.rstrip()) for j in line.split(' ')]
                seq_matrix = convert_dna_seq_to_matrix(one_dna_seq)
                dna_seq.append(seq_matrix)

            i = i + 1

        # convert DNA seq to matrix of 0s and 1s
        identity_matrix = np.eye(bases, dtype=int)
        forward = np.asarray(dna_seq)

        rev_seqs = []

        for fwd_seq in forward:  # for each fwd sequence
            fwd_seq_transpose = np.transpose(fwd_seq)
            rev = np.flip([identity_matrix[complement_base(np.argmax(i))].tolist() for i in fwd_seq_transpose], 0)
            rev = np.transpose(rev)
            rev_seqs.append(rev)

        reverse = np.asarray(rev_seqs)
        binding_value = np.asarray(binding_vals)

        np.save(forward_file + '.npy', forward)
        np.save(reverse_file + '.npy', reverse)
        np.save(bind_v_file + '.npy', binding_value)

        x_fwd = os.path.splitext(os.path.basename(forward_file + '.npy'))[0] + '.npy'
        x_rev = os.path.splitext(os.path.basename(reverse_file + '.npy'))[0] + '.npy'
        y = os.path.splitext(os.path.basename(bind_v_file + '.npy'))[0] + '.npy'

        return x_fwd, x_rev, y

    else: # not save (for evaluating test DNA sequences); should return the .npy arrays
        i = 1
        for line in file:
            one_dna_seq = [switch(j.rstrip()) for j in line.split(' ')]
            seq_matrix = convert_dna_seq_to_matrix(one_dna_seq)
            dna_seq.append(seq_matrix)
            i = i + 1

        # convert DNA seq to matrix of 0s and 1s
        identity_matrix = np.eye(bases, dtype=int)
        forward = np.asarray(dna_seq)

        rev_seqs = []

        for fwd_seq in forward:  # for each fwd sequence
            fwd_seq_transpose = np.transpose(fwd_seq)
            rev = np.flip([identity_matrix[complement_base(np.argmax(i))].tolist() for i in fwd_seq_transpose], 0)
            rev = np.transpose(rev)
            rev_seqs.append(rev)

        reverse = np.asarray(rev_seqs)

        return forward[0], reverse[0], None


def convert_csv_to_npy(csv_filepath, test=False):
    forward_file, reverse_file, bind_v_file = data_files(os.path.join(project_root, 'data'))

    file = open(csv_filepath, "r")

    dna_seq = []

    if not test:
        binding_vals = []

        i = 1
        for line in file:
            if (i % 2 == 0):  # i.e. every 2nd row contains the binding values
                binding_vals.append(float(line.rstrip()))
            else:
                one_dna_seq = [switch(i.rstrip()) for i in line.split(',')]
                seq_matrix = convert_dna_seq_to_matrix(one_dna_seq)
                dna_seq.append(seq_matrix)

            i = i + 1

        # convert DNA seq to matrix of 0s and 1s
        identity_matrix = np.eye(bases, dtype=int)
        forward = np.asarray(dna_seq)

        rev_seqs = []

        for fwd_seq in forward:  # for each fwd sequence
            fwd_seq_transpose = np.transpose(fwd_seq)
            rev = np.flip([identity_matrix[complement_base(np.argmax(i))].tolist() for i in fwd_seq_transpose], 0)
            rev = np.transpose(rev)
            rev_seqs.append(rev)

        reverse = np.asarray(rev_seqs)

        binding_value = np.asarray(binding_vals)

        np.save(forward_file + '.npy', forward)
        np.save(reverse_file + '.npy', reverse)
        np.save(bind_v_file + '.npy', binding_value)

        x_fwd = os.path.splitext(os.path.basename(forward_file + '.npy'))[0] + '.npy'
        x_rev = os.path.splitext(os.path.basename(reverse_file + '.npy'))[0] + '.npy'
        y = os.path.splitext(os.path.basename(bind_v_file + '.npy'))[0] + '.npy'

        return x_fwd, x_rev, y

    else:
        i = 1
        for line in file:
            one_dna_seq = [switch(i.rstrip()) for i in line.split(',')]
            seq_matrix = convert_dna_seq_to_matrix(one_dna_seq)
            dna_seq.append(seq_matrix)
            i = i + 1

        # convert DNA seq to matrix of 0s and 1s
        identity_matrix = np.eye(bases, dtype=int)
        forward = np.asarray(dna_seq)

        rev_seqs = []

        for fwd_seq in forward:  # for each fwd sequence
            fwd_seq_transpose = np.transpose(fwd_seq)
            rev = np.flip([identity_matrix[complement_base(np.argmax(i))].tolist() for i in fwd_seq_transpose], 0)
            rev = np.transpose(rev)
            rev_seqs.append(rev)

        reverse = np.asarray(rev_seqs)

        return forward[0], reverse[0], None

def gen_save_rev_seq(fwd_seq_filepath, test=False):
    fwd_seq_file_name = os.path.splitext(os.path.basename(fwd_seq_filepath))[0]
    fwd_seqs = np.load(fwd_seq_filepath)
    identity_matrix = np.eye(bases, dtype=int)
    rev_seqs = []

    for f in fwd_seqs:  # for each fwd sequence
        fwd_seq_transpose = np.transpose(f)
        rev = np.flip([identity_matrix[complement_base(np.argmax(i))].tolist() for i in fwd_seq_transpose], 0)
        rev = np.transpose(rev)
        rev_seqs.append(rev)

    reverse = np.asarray(rev_seqs)

    if not test:
        # name_int = fwd_seq_file_name[fwd_seq_file_name.find('_', 2) + 1:]
        rev_file_name = fwd_seq_file_name + '_reverse.npy'

        np.save(os.path.join(project_root, 'data', rev_file_name), reverse)

        return rev_file_name

    else:
        return reverse[0]


def choose_random_input_data():
    '''
    Looks in /data directory and counts total sets of randomly generated data and uniformly chooses one set to be used.
    Returns tuple of file names (x_forward_#.npy, x_reverse_#.npy, y_#.npy)
    '''

    i = 1
    # synbio_gui/python/main/src/gui/data
    while os.path.exists(os.path.join(project_root, 'data', 'x_forward_' + str(i) + '.npy')):
        i += 1

    choice = np.random.choice(np.arange(1, i), 1)[0]
    x_fwd = "x_forward_" + str(choice) + ".npy"
    x_rev = "x_reverse_" + str(choice) + ".npy"
    y = "y_" + str(choice) + ".npy"

    return (x_fwd, x_rev, y)


def check_avail_model_name(model_name):
    '''
    Checks if input model_name already exists in /models folder.
    Assumes that all files in /models folder have the appropriate file extension and should be checked against.
    Returns True or False.
    '''
    exists = False
    models_path = os.path.join(project_root, 'models')  # synbio_gui/python/main/src/gui/models

    if not os.path.exists(models_path):
        os.makedirs(models_path)

    # list of file names without extensions, e.g. "test1.txt" --> "test1"
    model_files = [os.path.splitext(os.path.basename(os.path.join(models_path, f)))[0] \
                   for f in os.listdir(models_path) if os.path.isfile(os.path.join(models_path, f))]

    try:
        exists_idx = model_files.index(model_name)
    except ValueError:
        exists_idx = -1

    if (exists_idx >= 0):
        exists = True

    return exists
