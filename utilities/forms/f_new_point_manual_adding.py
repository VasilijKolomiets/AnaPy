# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 15:02:56 2022

@author: manager
"""
from functools import partial  # TODO: replace lambda(s)

import tkinter as tk
from tkinter import ttk

# from settings import state_params

from model import add_row_values_to_DB


def entered_data_process(
    entered_data_processing,
        widget_dict_, *args):
    # params dict forming for 'entered_data_processing' call

    global root_frame

    field_value_dict = {
        k: v['type'](v['entry'].get()) for k, v in widget_dict_["entries"].items()
    }
    id_ = entered_data_processing(*args, field_value_dict)
    root_frame.destroy()


def new_point_manual_adding(
        widget_dict: dict = dict(),
        params_tuple_for_partial: tuple = tuple(),    # DB table name OR  DB table name & row ID
        entered_data_processing=add_row_values_to_DB,  # by default, save new row data to DB table
) -> None:
    """
    'widget_dict' structure:
        {
            "minsize": (1000, 500),
            "title": 'window title',

            # list of forms entries with their names:
            "entries": {
                entry_1_name: {'text': 'entry_1_name', 'type': type},
                entry_2_name: {'text': 'entry_2_name', 'type': type},
                ...
                entry_N_name: {'text': 'entry_N_name', 'type': type},

                },
            # for example: 'code_EDRPOU': {'text': 'Код ЄДРПОУ', 'type': int},
            #               code_EDRPOU - is a field name in DB,
            #               'Код ЄДРПОУ' - will be displayed on the form created.
        }
    """
    global root_frame

    root_frame = tk.Tk()
    # set default minsize:
    minsize = (1000, 500) if "minsize" not in widget_dict else widget_dict["minsize"]
    root_frame.minsize(*minsize)
    root_frame.title(widget_dict["title"])

    for i, key in enumerate(widget_dict["entries"]):
        widget_dict["entries"][key]['label'] = ttk.Label(
            root_frame,
            text=widget_dict["entries"][key]['text'],
            font=("Arial", 12)
        )
        widget_dict["entries"][key]['label'].grid(row=i, column=0, sticky=tk.W, padx=12)

        widget_dict["entries"][key]['entry'] = ttk.Entry(root_frame, width=30)
        widget_dict["entries"][key]['entry'].grid(row=i, column=1, pady=2, padx=20)

    # we are using 'i' value after loop finishing
    submit_btn = ttk.Button(
        root_frame,
        text='Додати поля до бази',
        command=partial(entered_data_process,
                        entered_data_processing, widget_dict,
                        *params_tuple_for_partial
                        )
    )
    submit_btn.grid(row=i+1, column=0, pady=10, padx=10, ipadx=40)

    clear_btn = ttk.Button(
        root_frame, text='Очистити введений текст',
        command=partial(clear_all_inputs, widget_dict))
    clear_btn.grid(row=i+1, column=1, pady=10, padx=10, ipadx=40)

    root_frame.mainloop()


def clear_all_inputs(widget_dict_):
    """Clear all Entry field values (empty texts)."""
    for key in widget_dict_["entries"].keys():
        widget_dict_["entries"][key]['entry'].delete(0, tk.END)
