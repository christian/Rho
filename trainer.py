from Algorithm import Algorithm
import platform
import sys

params = {
    'ALGORITHM'            : 'ISMF', # ISMF or RISMF

    'MIN_IMPROVEMENT'      : 0.0001,  # Minimum improvement required to continue current feature
    'LEARNING_RATE'        : 0.001,   # Learning rate
    'REG_FACTOR'           : 0.015,  
    'MAX_FEATURES'         : 1,      # Number of features to use; or factors
    'DEFAULT_FEATURE_VALUE': 0.1,     # Initialization value for features
    'SQR_INIT'             : 0.01,    # DEFAULT_FEATURE_VALUE * DEFAULT_FEATURE_VALUE
    'MAX_EPOCHS'           : 1,      # Max epochs per feature
    'MIN_EPOCHS'           : 1,

    'MAX_MOVIES'           : 1683,    # Movies in entire training set (+1)
    'MAX_USERS'            : 944,     # Users in entire training set (+1)
    'MAX_RATINGS'          : 100001,  # Ratings in entire training set (+1)

    'TRAINING_DATASET'     : 'dataset/u1.base',
    'TEST_DATASET'         : 'dataset/u1.test',
    'RECORD_RESULTS_TO_SQL': True,
}

if __name__ == "__main__":
    print 'Machine Details:'
    print '   Platform ID:  %s' % platform.platform()
    print '   Executable:   %s' % sys.executable
    print '   Python:       %s' % platform.python_version()
    print '   Compiler:     %s' % platform.python_compiler()

    train = Algorithm(params)
    train.run()