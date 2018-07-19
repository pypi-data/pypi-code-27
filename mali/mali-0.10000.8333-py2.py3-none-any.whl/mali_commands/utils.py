# -*- coding: utf8 -*-


def monitor_logs(ctx, url, disable_colors):
    from mali_commands.sse_firebase import LogsThread

    result = ctx.obj.handle_api(ctx.obj, ctx.obj.session, 'get', url)

    logs_thread = LogsThread(ctx.obj.config, result['url'], disable_colors)
    logs_thread.start()
    logs_thread.join()
