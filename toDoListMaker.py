from icalendar import Calendar
from datetime import datetime, timedelta
import pytz
import ics

def parse_ical_to_todo(ical_file_path, priority_thresholds=None):
    """
    Parse an iCal/ICS file and generate a prioritized to-do list
    priority_thresholds: dictionary with timedelta values for different priority levels
    e.g., {'high': 1, 'medium': 7, 'low': 30} (days)
    """
    if priority_thresholds is None:
        priority_thresholds = {
            'high': 1,      # Within 1 day
            'medium': 7,    # Within 1 week
            'low': 30       # Within 30 days
        }

    # Read the calendar file
    with open(ical_file_path, 'r', encoding='utf-8') as file:
        calendar = ics.Calendar(file.read())

    todos = []
    now = datetime.now(pytz.UTC)

    # Process each event in the calendar
    for event in calendar.events:
        event_summary = event.name
        event_start = event.begin.datetime
            
        # Convert datetime to UTC if it's not already
        if event_start.tzinfo is None:
            event_start = pytz.UTC.localize(event_start)

        # Calculate time until event
        time_until = event_start - now
            
        # Determine priority
        priority = 'none'
        for level, days in priority_thresholds.items():
            if time_until <= timedelta(days=days):
                priority = level
                break

        todos.append({
            'task': event_summary,
            'date': event_start,
            'priority': priority,
            'time_until': time_until
        })

    # Sort todos by date
    todos.sort(key=lambda x: x['date'])
    return todos

def display_todo_list(todos):
    """Display the todo list with color-coded priorities"""
    priority_colors = {
        'high': '\033[91m',    # Red
        'medium': '\033[93m',  # Yellow
        'low': '\033[92m',     # Green
        'none': '\033[0m'      # Default
    }
    reset_color = '\033[0m'

    print("\nPrioritized Todo List:")
    print("=====================")
    
    for todo in todos:
        color = priority_colors.get(todo['priority'], priority_colors['none'])
        print(f"{color}[{todo['priority'].upper()}] {todo['task']}")
        print(f"Date: {todo['date'].strftime('%Y-%m-%d %H:%M')} "
              f"(in {todo['time_until'].days} days){reset_color}")

def main():
    # Example usage
    ical_file_path = r"C:\Users\bergs\Downloads\bergs.isaiah@gmail.com.ical\Academic_Calendar@group.calendar.google.com.ics"
    
    # Custom priority thresholds (in days)
    priority_thresholds = {
        'high': 2,      # Within 2 days
        'medium': 7,    # Within 1 week
        'low': 14       # Within 2 weeks
    }
    
    try:
        todos = parse_ical_to_todo(ical_file_path, priority_thresholds)
        display_todo_list(todos)
    except FileNotFoundError:
        print(f"Error: Could not find calendar file at {ical_file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

# Test Test Test