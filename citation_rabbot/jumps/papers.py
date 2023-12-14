from .papers_query import author_papers_parser_add_arguments, papers_parser_add_arguments
from .papers_query import author_papers_args2querys, references_args2querys, citations_args2querys
from .papers_display import papers_results2message
author_papers_jump = (
    "author_papers",
    author_papers_parser_add_arguments,
    author_papers_args2querys,
    papers_results2message,
    None
)
references_jump = (
    "references",
    papers_parser_add_arguments,
    references_args2querys,
    papers_results2message,
    None
)
citations_jump = (
    "citations",
    papers_parser_add_arguments,
    citations_args2querys,
    papers_results2message,
    None
)
