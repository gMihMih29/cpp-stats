'''
Main file of project.
'''

import click
from cpp_stats.cpp_stats import CppStats

@click.command()
@click.option('--report', default='report.xml',
              help='Path to xml file where to store report.')
@click.argument('path_to_repo')
def main(path_to_repo, report):
    '''
    Main function of program that calculates metrics for a given 
    C/C++ repository and stores report in XML file.
    
    Parameters:
    path_to_repo (str): Path to the repository.
    report (str): Path to xml file where to store report.
    '''
    stats = CppStats(path_to_repo, True)
    with open(report, "w", encoding="utf-8") as f:
        click.echo(stats.as_xml(), file=f)

if __name__ == "__main__":
    # pylint: disable=E1120
    main()
