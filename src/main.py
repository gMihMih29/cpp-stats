import click
from cpp_stats import cpp_stats

@click.command()
@click.option('--report', default='report.xml', help='Path to xml file where to store report.')
@click.argument('path_to_repo')
def main(path_to_repo, report):
    stats = cpp_stats.CppStats(path_to_repo)
    with open(report, "w") as f:
        click.echo(stats.as_xml(), file=f)
    

if __name__ == "__main__":
    main()