from citation_rabbot.models import Jump
from .papers_query import author_papers_parser_add_arguments, papers_parser_add_arguments
from .papers_query import author_papers_args2querys, references_args2querys, citations_args2querys
from .papers_display import papers_results2message
author_papers_jump = Jump(
    name="author_papers",
    parser_add_arguments=author_papers_parser_add_arguments,
    args2querys=author_papers_args2querys,
    results2message=papers_results2message,
    description=None
)
references_jump = Jump(
    name="references",
    parser_add_arguments=papers_parser_add_arguments,
    args2querys=references_args2querys,
    results2message=papers_results2message,
    description=None
)
citations_jump = Jump(
    name="citations",
    parser_add_arguments=papers_parser_add_arguments,
    args2querys=citations_args2querys,
    results2message=papers_results2message,
    description=None
)
