
# Events

BEAT_EVENT = 1
BPM_CHANGE_EVENT = 2
GENDER_CHANGE_EVENT = 3
HARMONIC_CHANGE_EVENT = 4

EVENTS_PARAM = [
    (BEAT_EVENT, 'Beat'),
    (BPM_CHANGE_EVENT, 'BPM change'),
    (GENDER_CHANGE_EVENT, 'Gender change'),
    (HARMONIC_CHANGE_EVENT, 'Harmonic change'),
]

# Continuous

BPM_CONTINUOUS = 1
RMS_POWER_CONTINUOUS = 2

CONTINUOUS_PARAM = [
    (BPM_CONTINUOUS, 'BPM'),
    (RMS_POWER_CONTINUOUS, 'RMS Power'),
                ]

# Boolean
# Do not start at 0 !

VOICES_BOOLEAN = 1
GENDER_DISCO_BOOLEAN = 2
GENDER_SALSA_BOOLEAN = 3

BOOLEAN_PARAM = [('Genders', (
                        (GENDER_DISCO_BOOLEAN, 'Disco'),
                        (GENDER_SALSA_BOOLEAN, 'Salsa'),
                            )),
                 ('Others', (
                        (VOICES_BOOLEAN, 'Voices'),
                            ))
                  ]
