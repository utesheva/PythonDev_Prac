import calendar
import cmd

class numbername(cmd.Cmd):
    prompt = 'calend> '
    Month = {m.name: m.value for m in calendar.Month}

    def do_prmonth(self, arg):
        """Print a month’s calendar as returned by formatmonth()."""
        try:
            year = int(arg.split()[0])
            month = arg.split()[1]
            calendar.TextCalendar().prmonth(year, self.Month[month])
        except Exception as e:
            print(f'Invalid args: {e}')

    def do_pryear(self, arg):
        """Print the calendar for an entire year as returned by formatyear()."""
        try:
            year = int(arg.split()[0])
            calendar.TextCalendar().pryear(year)
        except Exception as e:
            print(f'Invalid arg: {e}')

    def do_EOF(self, args):
        return 1

    def complete_prmonth(self, text, line, begidx, endidx):
        return [c for c in self.Month if c.startswith(text)]

if __name__ == '__main__':
    numbername().cmdloop() 
