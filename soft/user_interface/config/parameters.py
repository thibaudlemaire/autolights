
# Events

BEAT_EVENT = 0
BPM_CHANGE_EVENT = 1
GENDER_CHANGE_EVENT = 2
HARMONIC_CHANGE_EVENT = 3

EVENTS_PARAM = [
    (BEAT_EVENT, 'Beat Event'),
    (BPM_CHANGE_EVENT, 'BPM change Event'),
    (GENDER_CHANGE_EVENT, 'Gender change Event'),
    (HARMONIC_CHANGE_EVENT, 'Harmonic change Event'),
]

# Continuous

BPM_CONTINUOUS = 0
RMS_POWER_CONTINUOUS = 1

CONTINUOUS_PARAM = [
    (BPM_CONTINUOUS, 'BPM'),
    (RMS_POWER_CONTINUOUS, 'RMS Power'),
                ]

# Boolean

VOICES_BOOLEAN = 0
GENDER_DISCO_BOOLEAN = 1
GENDER_SALSA_BOOLEAN = 2

BOOLEAN_PARAM = [('Genders', (
                        (GENDER_DISCO_BOOLEAN, 'Disco'),
                        (GENDER_SALSA_BOOLEAN, 'Salsa'),
                            )),
                 ('Others', (
                        (VOICES_BOOLEAN, 'Voices'),
                            ))
                  ]
