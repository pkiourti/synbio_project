import numpy as np
import os

###############################################
###############################################
# copied over from Penny's main.py temporarily
###############################################
###############################################
bases = 4


def data_files():
    i = 1
    while os.path.exists(os.path.join('data', 'x_forward_' + str(i) + '.npy')):
        i += 1

    if not os.path.exists('data'):
        os.makedirs('data')

    return (os.path.join('data', 'x_forward_' + str(i)),
            os.path.join('data', 'x_reverse_' + str(i)),
            os.path.join('data', 'y_' + str(i)))


def complement_base(idx):
    if idx == 0:
        return 1
    elif idx == 1:
        return 0
    elif idx == 2:
        return 3
    elif idx == 3:
        return 2

###############################################
###############################################
###############################################


def switch(argument):
    switcher = {
        "A": 0,
        "T": 1,
        "C": 2,
        "G": 3,
    }
    return switcher.get(argument, "Invalid base")


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
def convert_txt_to_npy(txt_filepath):
    forward_file, reverse_file, bind_v_file = data_files()

    file = open("dna_seq.txt", "r")

    dna_seq = []
    binding_vals = []

    i = 1
    for line in file:
        if (i % 2 == 0):  # i.e. every 2nd row contains the binding values
            binding_vals.append(line.rstrip())
        else:
            one_dna_seq = [switch(i.rstrip()) for i in line.split(' ')]
            seq_matrix = convert_dna_seq_to_matrix(one_dna_seq)
            dna_seq.append(seq_matrix)

        i = i + 1

    # convert DNA seq to matrix of 0s and 1s
    identity_matrix = np.eye(bases, dtype=int)
    forward = np.asarray(dna_seq)
    reverse = np.flip([identity_matrix[complement_base(np.argmax(i))].tolist() for i in forward], 0)
    binding_value = np.asarray(binding_vals)

    np.save(forward_file + '.npy', forward)
    np.save(reverse_file + '.npy', reverse)
    np.save(bind_v_file + '.npy', binding_value)


def convert_csv_to_npy(csv_filepath):
    forward_file, reverse_file, bind_v_file = data_files()

    file = open("dna_seq.txt", "r")

    dna_seq = []
    binding_vals = []

    i = 1
    for line in file:
        if (i % 2 == 0):  # i.e. every 2nd row contains the binding values
            binding_vals.append(line.rstrip())
        else:
            one_dna_seq = [switch(i.rstrip()) for i in line.split(',')]
            seq_matrix = convert_dna_seq_to_matrix(one_dna_seq)
            dna_seq.append(seq_matrix)

        i = i + 1

    # convert DNA seq to matrix of 0s and 1s
    identity_matrix = np.eye(bases, dtype=int)
    forward = np.asarray(dna_seq)
    reverse = np.flip([identity_matrix[complement_base(np.argmax(i))].tolist() for i in forward], 0)
    binding_value = np.asarray(binding_vals)

    np.save(forward_file + '.npy', forward)
    np.save(reverse_file + '.npy', reverse)
    np.save(bind_v_file + '.npy', binding_value)


def choose_random_input_data():
    '''
    Looks in /data directory and counts total sets of randomly generated data and uniformly chooses one set to be used.
    Returns tuple of file names (x_forward_#.npy, x_reverse_#.npy, y_#.npy)
    '''

    i = 1
    # synbio_gui/python/main/src/gui/data
    while os.path.exists(os.path.join('../../../../../data', 'x_forward_' + str(i) + '.npy')):
        i += 1

    choice = np.random.choice(np.arange(1,i+1), 1)
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
    models_path = '../../../../../models' # synbio_gui/python/main/src/gui/models

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