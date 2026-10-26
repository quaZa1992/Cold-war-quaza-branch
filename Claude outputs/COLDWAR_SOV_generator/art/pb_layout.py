# IMPERIA CW — Cold War: art — pb layout.
# COLDWAR | Layout of the Politburo dossier (decision category GUI). Shared by the art renderer (art/politburo_art.py)
# and the GUI generator (cw_pbgui.py), so the painted background and the dynamic elements line up exactly.
W, H = 510, 740

BANNER_H = 62                        # red banner with the emblem and the title
STRIP_Y = 66                         # typed file reference line

# General Secretary block: photo left, a typed form right
GS_PHOTO = (22, 98)                  # top-left of the portrait (GS_SCALE of a 156 x 210 leader portrait)
GS_SCALE = 0.70
GS_PW, GS_PH = round(156 * GS_SCALE), round(210 * GS_SCALE)   # 109 x 147
LABEL_X = 148                        # form labels
VALUE_X = 246                        # typed values
VALUE_W = 252
ROWS = {"office": 90, "name": 110, "heir": 140, "balance": 162, "cohesion": 184, "session": 206, "congress": 228}
ROW_H = 20
BAR = (VALUE_X, 167, 166, 10)        # balance track x, y, w, h (value text right of it)
BAR_FRAMES = 21                      # marker positions -1.0 ... +1.0 in steps of 0.1
BAR_PAD = 6                          # transparent margin of each marker frame left/right of the track

# republican seats
SEATS_HEAD_Y = 262
SEAT_Y = 288                         # top of the photo paper
SEAT_X = [14, 180, 346]              # left edge of each seat card
SEAT_W = 150
SEAT_SCALE = 0.50
SEAT_PW, SEAT_PH = round(156 * SEAT_SCALE), round(210 * SEAT_SCALE)   # 78 x 105
SEAT_PHOTO_DX, SEAT_PHOTO_DY = 6, 6  # portrait offset inside the photo paper
SEAT_FLAG_DX, SEAT_FLAG_DY = 96, 8   # flag position inside the card
SEAT_NAME_Y = SEAT_Y + 122
SEAT_TITLE_Y = SEAT_Y + 140

# ballot strip
BALLOT_Y = 474
BALLOT_H = 34

# socialist emulation
EMU_HEAD_Y = 514
EMU_ROW_Y = 548
EMU_ROW_H = 20
EMU_ROWS = ["growth", "industry", "output", "plan"]
EMU_COLS = {"icon": 16, "label": 38, "banner": 147, "flag": 164, "leader": 196, "value": 332, "rank": 428}   # banner: the Red Banner of the column
BANNER_W, BANNER_H_ = 15, 18         # the small banner sprite

# the honour roll under the table
HONOUR_ICON_X, HONOUR_TEXT_X = 14, 36
PRIDE_Y = EMU_ROW_Y + 4 * EMU_ROW_H + 6     # Pride of the Union (and its title)
LAG_Y = PRIDE_Y + 20                 # last place (left) and Moscow's favourite (right)
FAV_X = 232
SPART_Y = LAG_Y + 20                 # the Spartakiad of the Peoples of the USSR
FOOT_Y = SPART_Y + 22                # signature of the General Department and the archive stamp
