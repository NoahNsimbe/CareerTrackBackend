from pandas import Series

from app.serializers import CutOffPointsSerializer, CareerCoursesSerializer, CareersSerializer
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
    df = pd.read_csv("/home/noah/projects/career_track/career_track_backend/career_track/app/career_course_mappings.csv", header=None)

    for row in df.values:
        careers_string = str(row[0]).strip()
        careers = careers_string.split(",")

        for career in careers:

            career_data = {
                "name": career.strip().title(),
                "description": career.strip().title()
            }

            career_serializer = CareersSerializer(data=career_data)
            try:
                career_serializer.is_valid(raise_exception=True)
                # career_serializer.save()
            except Exception as ex:
                print(ex)


def load_mappings():
    df = pd.read_csv("/home/noah/projects/career_track/career_track_backend/career_track/app/career_course_mappings.csv", header=None)

    for row in df.values:
        careers_string = str(row[0]).strip()
        courses_string = str(row[1]).strip()

        careers = careers_string.split(",")
        courses = courses_string.split(",")

        for career in careers:

            for course in courses:
                data = {
                    "course": course.strip().upper(),
                    "career": career.strip().title()
                }

                serializer = CareerCoursesSerializer(data=data)
                try:
                    serializer.is_valid(raise_exception=True)
                    # serializer.save()
                except Exception as ex:
                    print(ex)


if __name__ == "__main__":
    load_careers()
