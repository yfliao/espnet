# We only need the NCTU parser stuff below for the optional text normalization(for LM-training) step
PARSER_ROOT=tools/new_parser_UNICODE
export PATH=$PATH:$PARSER_ROOT

# FaNT is needed for noise/phone
FANT_ROOT=tools/fant
export PATH=$PATH:$FANT_ROOT

# g729a/b is needed for noise/phone
G729_ROOT=tools/g729a
export PATH=$PATH:$G729_ROOT
