# Maia Knowledge scripts

Knowledge pipeline commands belong here. They read `docs/temes/` and write
intermediate files, JSONL and reports only to this dataset's sibling
directories. Shared Python logic lives in `src/training_data/`.

`generate_candidates.py` creates review drafts and coverage reports. Template
questions remain internal until a person rewrites and approves them. A source
with pending redistribution cannot enter public candidate messages or splits;
a source that forbids redistribution is excluded. If no records pass those
gates, the command leaves the split directory without empty train, validation
and test files.
