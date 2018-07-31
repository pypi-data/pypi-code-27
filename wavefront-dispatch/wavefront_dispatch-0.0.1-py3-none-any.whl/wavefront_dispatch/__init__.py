from pyformance import MetricsRegistry
from wavefront_pyformance.wavefront_reporter import WavefrontDirectReporter
import os
from datetime import datetime
from wavefront_pyformance import delta

reg = None

def wrapper(func):
    """
    Returns the Wavefront Dispatch wrapper. The wrapper collects dispatch functions
    standard metrics and reports it directly to the specified wavefront url. It
    requires the following Environment variables to be set:
    1.WAVEFRONT_URL : https://<INSTANCE>.wavefront.com
    2.WAVEFRONT_API_TOKEN : Wavefront API token with Direct Data Ingestion permission
    """
    def call_dispatch_function(wf_reporter, *args, **kwargs):

        METRICS_PREFIX = "dispatch.function.wf."
        # Register duration metrics
        dispatch_function_duration_gauge = reg.gauge(METRICS_PREFIX + "duration")
        # Register invocations metrics
        dispatch_function_invocations_counter = delta.delta_counter(reg, METRICS_PREFIX + "invocations")
        dispatch_function_invocations_counter.inc()
        # Registry errors metrics
        dispatch_erros_count = delta.delta_counter(reg, METRICS_PREFIX + "errors")
        time_start = datetime.now()
        try:
            response = func(*args, **kwargs)
            return response
        except:
            dispatch_erros_count.inc()
            raise
        finally:
            time_taken = datetime.now() - time_start
            dispatch_function_duration_gauge.set_value(time_taken.total_seconds() * 1000)
            wf_reporter.report_now(registry=reg)

    def wavefront_wrapper(*args, **kwargs):
        print("Func has been decorated.")

        # Initialize registry
        global reg
        reg = MetricsRegistry()

        # Get wavefront secrets
        context, payload = args[0], args[1]
        server = context["secrets"].get("wavefront_server_url", "")
        auth_token = context["secrets"].get("wavefront_auth_token", "")

        # Initialize the wavefront direct reporter
        wf_direct_reporter = WavefrontDirectReporter(server=server,
                                                     token=auth_token,
                                                     registry=reg,
                                                     prefix="")

        call_dispatch_function(wf_direct_reporter,
                               *args,
                               **kwargs)

    return wavefront_wrapper


def get_registry():
    return reg