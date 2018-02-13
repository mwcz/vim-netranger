import vim


def walk(fn, obj, *args, **kwargs):
    """Recursively walk an object graph applying `fn`/`args` to objects."""
    if int(vim.eval('has("nvim")')):
        return obj
    objType = type(obj)
    if objType in [list, tuple, vim.List]:
        return list(walk(fn, o, *args) for o in obj)
    elif objType in [dict, vim.Dictionary]:
        return dict((walk(fn, k, *args), walk(fn, v, *args)) for k, v in obj.items())
    return fn(obj, *args, **kwargs)


def decode_if_bytes(obj, mode=True):
    """Decode obj if it is bytes."""
    if mode is True:
        mode = 'strict'
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors=mode)
    return obj


def VimVar(name):
    return walk(decode_if_bytes, vim.vars[name])


def VimErrorMsg(exception):
    if hasattr(exception, 'output'):
        msg = exception.output.decode('utf-8')
    else:
        msg = str(exception)
    vim.command('echohl ErrorMsg | echo "{}" | echohl None '.format(msg.replace('"','\\"')))


def VimWarningMsg(msg):
    vim.command('echohl WarningMsg | echo "{}" | echohl None '.format(msg.replace('"','\\"')))


def VimUserInput(hint, default=''):
    vim.command('let g:NETRRegister=input("{}: ", "{}")'.format(hint, default))
    return decode_if_bytes(vim.vars['NETRRegister'])


def VimCurWinWidth():
    return vim.current.window.width
