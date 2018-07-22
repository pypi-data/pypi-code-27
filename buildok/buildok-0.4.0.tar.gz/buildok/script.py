# Copyright 2018 Alexandru Catrina
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import print_function

from timeit import default_timer
from os import getpid

from buildok.statement import Statement
from buildok.converter import Converter
from buildok.matcher import Matcher
from buildok.reader import Reader
from buildok.report import Report

from buildok.readers.read_me import ReadmeReader
from buildok.structures.topic import Topic
from buildok.statements.invoke import InvokeTopic
from buildok.util.log import Log


RUN_INSTRUCTIONS = """
    Buildok is ready! Choose a topic to run, either by it's ID or by name (can
    be partial match as well). During the runtime ^C (SIGINT) is ignored. Typing
    an ID or a name that does not exist will restart the promter. Leaving the
    field blank will end session.
"""

WARNING_UNSAFE_SHELL = u"""\033[91m
    Detected --unsafe-shell option! Use this option on your own risk only if you
    really know what you're doing! Please check documentation if you're not sure
    what --unsafe-shell is, or better yet, remove it and update your guide.\033[0m
"""

class Script(object):
    """Automated script wrapper.

    Args:
        args         (list): List of shell arguments.
        topic         (str): Topic as a text string.
        steps        (list): List of topic steps.
        last_step     (int): Last step index.
        guide_topics (list): List of guide topics.
        convert      (bool): Convertion flag.
    """

    def __init__(self, args):
        self.args = args
        self.topic = None
        self.steps = None
        self.last_step = 0
        self.guide_topics = None
        self.convert = False
        self.fake_run = False
        Log.info("Initializing...")

    def setup(self):
        """Setup project path, topic and topic pattern, convertion type.
        """

        # Look for a specific topic
        if self.args.topic is not None:
            Topic.set_project_topic(self.args.topic)
            Log.info("Topic changed to: %s" % self.args.topic)

        # Set topic pattern
        if self.args.topic_pattern is not None:
            Topic.set_project_topic_pattern(self.args.topic_pattern)
            Log.info("Topic pattern changed to: %s" % self.args.topic_pattern)

        # Change project path from current working directory to choosen path
        if self.args.guide is not None:
            Reader.set_project_path(self.args.guide)
            Log.info("Project guide location: %s" % self.args.guide)

        # Convert build steps to script before exit
        if self.args.convert is not None:
            Converter.prepare(self.args.convert)
            Log.info("Topic convertion set to: %s" % self.args.convert)
            self.convert = True

        # Toggle fake run
        self.fake_run = self.args.fake_run

    def run(self, ignore_fails=False):
        """Run all steps for the current selected topic.
        """

        if self.fake_run:
            Log.info("Topic '%s' faked run" % self.topic.get_title())
            Report.set_status("FAKED")
        else:
            self.launch_topic(ignore_fails)

        if self.convert:
            self.launch_convertion()

    def launch_convertion(self):
        """Convert build steps to target convertion.
        """

        Log.debug("Converting...")
        Converter.check() and Converter.save(self.steps)
        Log.debug("Conversion done!")

    def launch_topic(self, ignore_fails=False, failed=False):
        """Launch topic and run all steps.
        """

        Log.info("Preparing to run %d steps from topic..." % len(self.topic.get_steps()))

        # Loop steps and run each one
        start_time = default_timer()
        Log.debug("Setting start time: %s" % start_time)

        for self.last_step, step in enumerate(self.steps):
            Log.debug("Preparing step (%d) %s" % (self.last_step+1, step.get_description()))
            Log.info(u"Running \033[93m%s\033[0m ..." % step.get_step())
            try:
                success, output = step.run()
                if success:
                    Log.info(u"\033[92m\u2713 (Success)\033[0m \033[93m%s\033[0m" % output)
                else:
                    Log.info(u"\033[91m? (Failed)\033[0m \033[95m%s\033[0m" % output)
                    if not ignore_fails:
                        failed = True
                        Report.set_error(output)
                        break
                Report.inc_step(1)
            except KeyboardInterrupt:
                Log.info("Stopping current step...")
                Log.warn("Interrupting may lead to unexpected results")
                Log.debug("Stop master process at your own risk (PID %s)" % getpid())
            except Exception as e:
                failed = True
                Report.set_error(e)
                Log.info(u"\033[91m? (Error) %s\033[0m" % str(e))
                break

        stop_time = default_timer()
        Log.debug("Set stop time: %s" % stop_time)
        Log.debug("Runtime %ss" % (stop_time - start_time))

        # Save runtime
        Report.set_runtime(stop_time - start_time)

        # Wrap up...
        Log.debug("Done running steps...")
        if failed:
            Log.info("An error occured while topic '%s' was running" % self.topic.get_title())
            Report.set_status("Failed")
        else:
            Log.info("Topic '%s' has ran all steps with no errors" % self.topic.get_title())
            Report.set_status("OK")
        Log.debug("Closing...")

    def parse(self):
        """Parse guide and extract topics.

        User prompter asks to choose a topic from the selection in order to know
        what steps are queued.
        """

        rr = ReadmeReader(validate=True)
        rr.read()
        rr.parse()
        Log.info("Parsing guide...")

        # Preview scanned guide
        if self.args.preview:
            Log.info("Loading guide preview...")
            rr.preview(150)

        # Scan guide for topics
        guide = rr.get_guide() if self.args.topic is None else rr.get_guide_by_topic()
        if guide is None:
            Log.fatal("Guide has no such topic")

        # Pair each step with appropriate statement
        self.guide_topics = guide.get_topics()
        if self.args.strict:
            if not all([Matcher.pair_all(t.get_steps()) for t in self.guide_topics]):
                Report.set_status("Halted")
                Report.set_error("Unsupported steps")
                Log.fatal("Cannot continue because of unsupported steps")
        else:
            for t in self.guide_topics:
                for step in t.get_steps():
                    pair = Matcher.pair_one(step)
                    if not pair:
                        self.guide_topics.remove(t)

        # Scan topics
        topic, steps = None, []
        topics = [t.get_title() for t in guide.get_topics()]
        topics_len = len(topics)

        # Handle no topics
        if topics_len == 0:
            Log.fatal("No topics found")
        else:
            Log.info("Guide has %d topics" % topics_len)

        # Handle topics
        Log.info("Found the following topics...")
        print("")
        for pos, name in enumerate(topics):
            print(("%" + str(len(str(topics_len))+5) + "d) %s") % (pos+1, name))
        print(RUN_INSTRUCTIONS)

        # Display warnings
        if self.args.unsafe_shell:
            print(WARNING_UNSAFE_SHELL)

        # Save topic and topic's steps
        self.topic = self.get_user_input()
        self.steps = self.topic.get_steps()

        # Confirm topic
        print("")
        Log.info(u"Matching topic \033[92m%s\033[0m" % self.topic.get_title())

        # Patch topic imports
        self.patch_topic_invoke(self.steps)

        # Prepare report
        Report.set_total_steps(len(self.steps))
        Report.set_topic(self.topic.get_title())
        return self

    def patch_topic_invoke(self, steps):
        """Scan steps for topic invoking.

        Replace invoker step with topic's steps.
        """

        for i, step in enumerate(steps):

            # Skip if step is not an invoker
            if step.action is not InvokeTopic:
                continue

            # Find invoked topic
            topic = step.get_kwarguments().get("topic", "")
            topic_steps = self.get_steps_by_topic(topic)
            self.patch_topic_invoke(topic_steps)
            self.steps[i:i+1] = topic_steps

    def get_steps_by_topic(self, topic_name):
        """Retrieve steps by topic name.

        Returns an empty list if nothing is found.
        """

        for topic in Topic.get_all_topics():
            if topic_name.lower() == topic.get_title().lower():
                return topic.get_steps()
        return []


    def get_user_input(self, attempt=0):
        """Prompt user to choose a topic from a list.

        Exists if user leaves blank input or hits C^, otherwise continues until
        it receives a valid topic.
        """

        # Prompt for input
        try:
            if attempt > 0:
                print("") # spacing only
            user_input = raw_input("    >>> choose topic: ")
            attempt += 1

        # Exit on C^
        except KeyboardInterrupt:
            print("") # append newline after ^C
            Report.set_status("Exit")
            raise Exception

        # Exit on blank input
        if len(user_input) == 0:
            Report.set_status("Exit")
            raise Exception

        # Validate index or start over
        try:
            pos = int(user_input)
            if pos <= 0 or pos > len(self.guide_topics):
                raise IndexError
            return self.guide_topics[pos-1]
        except IndexError:
            print("    <<< topic #%d not found" % pos)
            return self.get_user_input(attempt)
        except Exception:
            pass

        # Validate full or partial topic name or start over
        try:
            topic = unicode(user_input)
            partial_match = None
            drop_partial = False
            for each in self.guide_topics:
                if each.get_title().strip() == topic.strip():
                    return each
                if partial_match is not None and each.get_title().startswith(topic) and not drop_partial:
                    drop_partial = True
                if partial_match is None and each.get_title().startswith(topic):
                    partial_match = each
            if not drop_partial and partial_match is not None:
                return partial_match
            print("    <<< topic \"%s\" not found" % topic)
        except Exception:
            pass

        # No valid topic found, start over
        return self.get_user_input(attempt)

    def print_report(self):
        """Dumps a report of the script outcome.
        """

        Log.info("Preparing to print report...")
        Report.output()
