from datetime import date, timedelta
import calendar
import psycopg2


def create_date_dimension(
    start_date,
    end_date
):

    connection = psycopg2.connect(
        host="postgres",
        port=5432,
        database="ecommerce",
        user="ecommerce",
        password="ecommerce"
    )

    cursor = connection.cursor()

    current_date = start_date

    while current_date <= end_date:

        date_key = int(
            current_date.strftime("%Y%m%d")
        )

        year = current_date.year

        quarter = (
            (current_date.month - 1)
            // 3
        ) + 1

        month = current_date.month

        month_name = calendar.month_name[
            current_date.month
        ]

        day = current_date.day

        day_name = current_date.strftime(
            "%A"
        )

        week_of_year = int(
            current_date.strftime("%U")
        )

        cursor.execute(
            """
            INSERT INTO dim_date (
                date_key,
                full_date,
                year,
                quarter,
                month,
                month_name,
                day,
                day_name,
                week_of_year
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            ON CONFLICT (date_key)
            DO NOTHING
            """,
            (
                date_key,
                current_date,
                year,
                quarter,
                month,
                month_name,
                day,
                day_name,
                week_of_year
            )
        )

        current_date += timedelta(
            days=1
        )

    connection.commit()

    cursor.close()
    connection.close()

    print(
        "Date dimension created successfully."
    )


if __name__ == "__main__":

    create_date_dimension(
        date(2025, 1, 1),
        date(2027, 12, 31)
    )