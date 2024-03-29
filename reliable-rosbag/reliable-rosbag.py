import rosbag
import numpy as np
import click
import matplotlib.pyplot as plt
from rich import print as rprint
from rich.console import Console
from rich.table import Table

def available_topics(rosbag_path):
    """List available topics in a rosbag."""
    try:
        with rosbag.Bag(rosbag_path) as bag:
            topics = list(bag.get_type_and_topic_info().topics.keys())
        return topics
    except Exception as e:
            # raise click.ClickException(f"{Fore.RED}Error listing rosbag topics: {e}{Style.RESET_ALL}")
            raise click.ClickException(f"[bold red]Error listing rosbag topics: {e}[\bold red]")


@click.command()
@click.argument('rosbag_path', type=click.Path(exists=True))
@click.option('--topics', '-t', multiple=True, required=True, help='ROS topics of interest')
@click.option('--measure', '-m', default='std', type=click.Choice(['std', 'var']), help='Volatility measure to consider (std or var)')
@click.option('--thres', '-th', type=float, default=0.5, help='Threshold value for validation')
def is_rosbag_valid(rosbag_path, topics: list, measure, thres):
    """Collect timestamps of consecutive messages for each specified topic."""
    is_reliable = True
    try:
        topic_timestamps = {}
        rows = []
        for selected_topic in topics:
            timestamps = []
            
            if selected_topic not in available_topics(rosbag_path):
                
                rprint(f"[bold red]Topic {selected_topic} not in available topics![/bold red]")
                user_input = click.prompt('Do you want to list all the available topics?', type=str)
                if user_input.lower() == 'yes':
                    click.echo(f"Available topics: {available_topics(rosbag_path)}")
                
                raise click.ClickException(f"Topic not found!")

            with rosbag.Bag(rosbag_path) as bag:
                for _, _, timestamp in bag.read_messages(topics=[selected_topic]):
                    timestamps.append(timestamp.to_sec())

            if measure == 'std':
                res = np.std(np.diff(timestamps))
            elif measure == 'var':
                res = np.var(np.diff(timestamps))
            else:
                raise click.ClickException(f"Invalid measure specified. Use 'std' or 'var'.")
            click.echo(f"\nTopic: {selected_topic}")
            # click.echo(f"Number of messages: {len(timestamps)}")
            # click.echo(f"Parameters: {measure} with threshold: {thres}")
            # click.echo(f"Result: {res:.2f}")
            if res > thres:
                is_reliable = False

            rows.append([selected_topic, measure, f"{thres}", f"{res:.2f}", "Reliable" if is_reliable else "Unreliable"])
            user_input = click.prompt('Do you want to plot it? (yes/no)', type=str)
            # user_input = "no"
            if user_input.lower() == 'yes':
                plt.figure()
                plt.plot(timestamps)
                plt.title(f"{selected_topic}")
                plt.xlabel('Message Index')
                plt.ylabel('TimeStamp (seconds)')
                plt.show()
            
                
        table = Table(title="Results")               

        columns = ["TopicName", "Measure", "Max Threshold", "Value", "Result"]

        for column in columns:
            table.add_column(column)

        for row in rows:
            table.add_row(*row, style='bright_green')

        console = Console()
        console.print(table)
        if not is_reliable:
            rprint(f"[bold red]Unreliable ROSBAG: {rosbag_path}![/bold red]")
        else:
            rprint(f"[bold green]Reliable ROSBAG: {rosbag_path}![/bold green]")
    except Exception as e:
        click.echo(f"Error processing rosbag: {e}")
        raise click.Abort()

if __name__ == '__main__':

    # Create a console instance
    console = Console()

    # Display an introduction message
    console.print("[bold underline]ROS Bag Analysis CLI[/bold underline]", style="bold magenta")
    console.print("Welcome to the ROS Bag Analysis CLI tool. This tool analyzes the reliability of a ROS bag file based on specified topics and timestamp measures.", style="green")
    console.print("A ROS Bag is labeled as 'reliable' when none of the given topics show a fluctuation (in terms of defined measure) lower then the set threshold", style="green")

    # Display usage information
    console.print("[bold]Usage:[/bold] python your_script.py <rosbag_path> --topics <topic1> <topic2> ... [options]", style="cyan")
    console.print("Example: python your_script.py /path/to/rosbag.bag --topics /sensor/data --measure std --thres 0.5", style="cyan")

    # Display available options
    console.print("\n[bold]Options:[/bold]", style="cyan")
    console.print("--topics, -t  [cyan]   Specify ROS topics of interest (multiple allowed)[/cyan]")
    console.print("--measure, -m [cyan]   Choose measure type ('std' or 'var')[/cyan]")
    console.print("--thres, -th  [cyan]   Max threshold of the defined measure[/cyan]")

    # Provide additional information or instructions
    console.print("\n[bold]Additional Information:[/bold]", style="cyan")
    console.print(" - The tool calculates the standard deviation ('std') or variance ('var') of timestamp differences for each specified topic.")
    console.print(" - Results are displayed in a table, and unreliable ROS bags are highlighted in [bold red]red[/bold red].")
    console.print(" - Optionally, you can plot the timestamp data for each specified topic.")

    # Display a separator
    console.print("\n[bold]-----------------------------------------[/bold]\n", style="magenta")

    # Add any other specific information or usage instructions if needed

    is_rosbag_valid()
