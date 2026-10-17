package enterprise.security.pii

default allow_vector_storage = false

# Allow ingestion only if raw unmasked PII is absent and sanitization was performed
allow_vector_storage {
    not contains_raw_ssn
    not contains_raw_credit_card
    not is_quarantined
    sanitization_verified
}

contains_raw_ssn {
    regex.match(`\b\d{3}-\d{2}-\d{4}\b`, input.chunk_text)
}

contains_raw_credit_card {
    regex.match(`\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b`, input.chunk_text)
}

is_quarantined {
    input.quarantined == true
}

sanitization_verified {
    input.sanitization_status == "COMPLETED"
}
