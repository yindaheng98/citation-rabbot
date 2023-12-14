from .papers_query import author_papers_parser, papers_parser
from .papers_query import author_papers_args2querys, references_args2querys, citations_args2querys
from .papers_display import papers_results2message
author_papers_jump = ("author_papers", author_papers_parser, author_papers_args2querys, papers_results2message, None)
references_jump = ("references", papers_parser, references_args2querys, papers_results2message, None)
citations_jump = ("citations", papers_parser, citations_args2querys, papers_results2message, None)
