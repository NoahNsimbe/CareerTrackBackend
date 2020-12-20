from pandas import Series

from app.serializers import CutOffPointsSerializer
import pandas as pd


def load_cut_toff_points():
    df = pd.read_csv("/home/noah/projects/career_track/career_track_backend/career_track/app/2020-GOV.csv", header=None)

    for row in df.values:
        data = {
            "course": str(row[1]).strip(),
            "points": float(str(row[2]).strip()),
            "year": 2020,
            "type": str(row[4]).strip(),
            "gender": str(row[3]).strip()
        }

        serializer = CutOffPointsSerializer(data=data)
        try:

            serializer.is_valid(raise_exception=True)
            # serializer.save()
        except Exception:
            print(row)

        # print(serializer.is_valid())
        #
        # serializer.save()


def load_careers():
    pass


if __name__ == "__main__":
    load_cut_toff_points()
