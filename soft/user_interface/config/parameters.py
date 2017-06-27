
# Events

BEAT_EVENT = 1
BPM_CHANGE_EVENT = 2
GENDER_CHANGE_EVENT = 3
HARMONIC_CHANGE_EVENT = 4
DROP_EVENT = 5

EVENTS_PARAM = [
    (BEAT_EVENT, 'Beat'),
    (BPM_CHANGE_EVENT, 'BPM change'),
    (GENDER_CHANGE_EVENT, 'Gender change'),
    (HARMONIC_CHANGE_EVENT, 'Harmonic change'),
    (DROP_EVENT, 'Drop'),
]

# Continuous

BPM_CONTINUOUS = 1
RMS_POWER_CONTINUOUS = 2
TUNING_CONTINUOUS = 3


CONTINUOUS_PARAM = [
    (BPM_CONTINUOUS, 'BPM'),
    (RMS_POWER_CONTINUOUS, 'RMS Power'),
    (TUNING_CONTINUOUS, 'Tuning'),
]

# Boolean
# Do not start at 0 !

VOICES_BOOLEAN = 1
GENDER_DISCO_BOOLEAN = 2
GENDER_LATINO_BOOLEAN = 3
GENDER_TECHNO_BOOLEAN = 4
GENDER_EDM_BOOLEAN = 5
GENDER_RETRO_BOOLEAN = 6


BOOLEAN_PARAM = [('Genders', (
                        (GENDER_DISCO_BOOLEAN, 'Disco'),
                        (GENDER_LATINO_BOOLEAN, 'Latino'),
                        (GENDER_TECHNO_BOOLEAN, 'Techno'),
                        (GENDER_EDM_BOOLEAN, 'EDM'),
                        (GENDER_RETRO_BOOLEAN, 'Retro'),
)),
                 ('Others', (
                        (VOICES_BOOLEAN, 'Voices'),
                            ))
                  ]
