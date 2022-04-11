

def total_ec_comparison(base, val1, val2, val1_db, val2_db):
    str = [
        checker(base, val1, val1_db,),
        "\n",
        checker(base, val2, val2_db),
    ]
    return str

def checker(base, val, val_db):
    if base <=  val:
        val1_percent = (val/base) * 100
        return "{} is 🔺 by +{:,.2f}%, ".format(val_db, val1_percent)
    else:
        val1_percent = (val/base) * 100
        return "{} is 🔻 by {:,.2f}%".format(val_db, val1_percent)

