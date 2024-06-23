from argparse import ArgumentParser

def getCmdArgs():
    parser = ArgumentParser(prog = 'resumeBuilder')

    parser.add_argument(
        'resumeFile',
        type = str,
        help = 'The YAML file containing the resume information',
        default = 'resume.yaml'
    )

    parser.add_argument(
        '-of', 
        '--order-file',
        type = str,
        required = False,
        dest = 'orderFile'
    )

    parser.add_argument(
        '-b',
        '--build-type',
        type = str,
        required = False,
        dest = 'buildType'
    )

    parser.add_argument(
        '-sf',
        '--split-files',
        required = False,
        dest = 'splitFiles',
        action = 'store_true'
    )

    parser.add_argument(
        '-r',
        '--recompile',
        required = False,
        action = 'store_true'
    )

    parser.add_argument(
        '-nc',
        '--no-compile',
        required = False,
        dest = 'noCompile',
        action = 'store_true',
        help = 'do not compile the tex files'
    )

    parser.add_argument(
        '-nw',
        '--no-write',
        required = False,
        dest = 'noWrite',
        action = 'store_true',
        help = 'do not write the tex files'
    )


    return parser.parse_args()

if __name__ == "__main__":
    print(getCmdArgs().resumeFile)
