#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Motus_game version 1.0
#  Created by Ingenuity i/o on 2023/10/20
#
# "no description"
#

import getopt
import signal
import sys
import time
import traceback
from pathlib import Path

from Motus_game import *

port = 5670
agent_name = "Motus_game"
device = None
verbose = False
is_interrupted = False
NB_TRY = 1

short_flag = "hvip:d:n:"
long_flag = ["help", "verbose", "interactive_loop", "port=", "device=", "name="]

ingescape_path = Path("~/Documents/Ingescape").expanduser()


def print_usage():
    print("Usage example: ", agent_name, " --verbose --port 5670 --device device_name")
    print("\nthese parameters have default value (indicated here above):")
    print("--verbose : enable verbose mode in the application (default is disabled)")
    print("--port port_number : port used for autodiscovery between agents (default: 31520)")
    print("--device device_name : name of the network device to be used (useful if several devices available)")
    print("--name agent_name : published name for this agent (default: ", agent_name, ")")
    print("--interactive_loop : enables interactive loop to pass commands in CLI (default: false)")


def print_usage_help():
    print("Available commands in the terminal:")
    print("	/quit : quits the agent")
    print("	/help : displays this message")


def return_iop_value_type_as_str(value_type):
    if value_type == igs.INTEGER_T:
        return "Integer"
    elif value_type == igs.DOUBLE_T:
        return "Double"
    elif value_type == igs.BOOL_T:
        return "Bool"
    elif value_type == igs.STRING_T:
        return "String"
    elif value_type == igs.IMPULSION_T:
        return "Impulsion"
    elif value_type == igs.DATA_T:
        return "Data"
    else:
        return "Unknown"


def return_event_type_as_str(event_type):
    if event_type == igs.PEER_ENTERED:
        return "PEER_ENTERED"
    elif event_type == igs.PEER_EXITED:
        return "PEER_EXITED"
    elif event_type == igs.AGENT_ENTERED:
        return "AGENT_ENTERED"
    elif event_type == igs.AGENT_UPDATED_DEFINITION:
        return "AGENT_UPDATED_DEFINITION"
    elif event_type == igs.AGENT_KNOWS_US:
        return "AGENT_KNOWS_US"
    elif event_type == igs.AGENT_EXITED:
        return "AGENT_EXITED"
    elif event_type == igs.AGENT_UPDATED_MAPPING:
        return "AGENT_UPDATED_MAPPING"
    elif event_type == igs.AGENT_WON_ELECTION:
        return "AGENT_WON_ELECTION"
    elif event_type == igs.AGENT_LOST_ELECTION:
        return "AGENT_LOST_ELECTION"
    else:
        return "UNKNOWN"


def signal_handler(signal_received, frame):
    global is_interrupted
    print("\n", signal.strsignal(signal_received), sep="")
    is_interrupted = True


def on_agent_event_callback(event, uuid, name, event_data, my_data):
    try:
        motus_game = my_data
        assert isinstance(motus_game, MotusGame)
        # add code here if needed
    except:
        print(traceback.format_exc())


def on_freeze_callback(is_frozen, my_data):
    try:
        motus_game = my_data
        assert isinstance(motus_game, MotusGame)
        # add code here if needed
    except:
        print(traceback.format_exc())


# inputs
def word_input_callback(iop_type, name, value_type, value, my_data):
    try:
        motus_game = my_data
        assert isinstance(motus_game, MotusGame)
        motus_game.wordI = value

        SQUARE_WIDTH = 100.0
        SQUARE_HEIGHT = 100.0
        FIRST_SQUARE_X = 100.0
        FIRST_SQUARE_Y = 80.0
        OFFSET_SQUARE = 100.0
        SPACE_BETWEEN_SQUARE = 10.0

        for index, letter in enumerate(motus_game.wordI):
            # display rect
            arguments_shape = (
                "rectangle",
                FIRST_SQUARE_X + index * OFFSET_SQUARE,
                FIRST_SQUARE_Y + (SQUARE_HEIGHT * (motus_game.nb_try - 1)) + SPACE_BETWEEN_SQUARE,
                SQUARE_WIDTH,
                SQUARE_HEIGHT,
                motus_game.get_color_by_letter(letter, index), "black", 1.0)
            igs.service_call("Whiteboard", "addShape", arguments_shape, "")

            arguments_text = (
                str(letter),
                FIRST_SQUARE_X + index * OFFSET_SQUARE + (SQUARE_WIDTH / 3),
                FIRST_SQUARE_Y + (SQUARE_HEIGHT * (motus_game.nb_try - 1)) + SPACE_BETWEEN_SQUARE + (SQUARE_WIDTH / 3),
                "#000000")
            igs.service_call("Whiteboard", "addText", arguments_text, "")

        igs.service_call("Whiteboard", "chat", "You tried : " + motus_game.wordI, "")
        motus_game.incr_nb_try()

        if motus_game.is_win():
            igs.service_call("Whiteboard", "clear", None, "")
            igs.service_call("Whiteboard", "chat", "You win !", "")
            motus_game.reset_game()
        else:
            if motus_game.is_lose():
                igs.service_call("Whiteboard", "clear", None, "")
                igs.service_call("Whiteboard", "chat", "You lose :(", "")
                motus_game.reset_game()









    except:
        print(traceback.format_exc())


if __name__ == "__main__":

    # catch SIGINT handler before starting agent
    signal.signal(signal.SIGINT, signal_handler)
    interactive_loop = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_flag, long_flag)
    except getopt.GetoptError as err:
        igs.error(err)
        sys.exit(2)
    for o, a in opts:
        if o == "-h" or o == "--help":
            print_usage()
            exit(0)
        elif o == "-v" or o == "--verbose":
            verbose = True
        elif o == "-i" or o == "--interactive_loop":
            interactive_loop = True
        elif o == "-p" or o == "--port":
            port = int(a)
        elif o == "-d" or o == "--device":
            device = a
        elif o == "-n" or o == "--name":
            agent_name = a
        else:
            assert False, "unhandled option"

    igs.agent_set_name(agent_name)
    igs.definition_set_version("1.0")
    igs.log_set_console(verbose)
    igs.log_set_file(True, None)
    igs.log_set_stream(verbose)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    if device is None:
        # we have no device to start with: try to find one
        list_devices = igs.net_devices_list()
        list_addresses = igs.net_addresses_list()
        if len(list_devices) == 1:
            device = list_devices[0]
            igs.info("using %s as default network device (this is the only one available)" % str(device))
        elif len(list_devices) == 2 and (list_addresses[0] == "127.0.0.1" or list_addresses[1] == "127.0.0.1"):
            if list_addresses[0] == "127.0.0.1":
                device = list_devices[1]
            else:
                device = list_devices[0]
            print("using %s as de fault network device (this is the only one available that is not the loopback)" % str(
                device))
        else:
            if len(list_devices) == 0:
                igs.error("No network device found: aborting.")
            else:
                igs.error("No network device passed as command line parameter and several are available.")
                print("Please use one of these network devices:")
                for device in list_devices:
                    print("	", device)
                print_usage()
            exit(1)

    agent = MotusGame()

    igs.observe_agent_events(on_agent_event_callback, agent)
    igs.observe_freeze(on_freeze_callback, agent)

    igs.input_create("word", igs.STRING_T, None)

    igs.observe_input("word", word_input_callback, agent)

    # todo add a new service if we want the return value (elementCreated)
    # igs.service_init("elementCreated", )

    igs.start_with_device(device, port)
    # catch SIGINT handler after starting agent
    signal.signal(signal.SIGINT, signal_handler)

    if interactive_loop:
        print_usage_help()
        while True:
            command = input()
            if command == "/quit":
                break
            elif command == "/help":
                print_usage_help()
    else:
        while (not is_interrupted) and igs.is_started():
            time.sleep(2)

    if igs.is_started():
        igs.stop()
