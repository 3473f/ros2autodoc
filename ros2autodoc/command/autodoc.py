from ros2cli.command import CommandExtension, add_subparsers_on_demand


class AutodocCommand(CommandExtension):
    """Various auotdoc related subcommands."""

    def add_arguments(self, parser, cli_name):
        self._subparser = parser
        add_subparsers_on_demand(
            parser, cli_name, "_verb", "ros2autodoc.verb", required=False
        )

    def main(self, *, parser, args):
        if not hasattr(args, "_verb"):
            # in case no verb was passed
            self._subparser.print_help()
            return 0

        extensions = args._verb

        # call the verb's main method
        return extensions.main(args=args)
