def c_to_f: . * 9 / 5 + 32;

. | { value: (.[$prop] | c_to_f | . * 100 | trunc | . / 100), created_at: (now | todateiso8601) }
