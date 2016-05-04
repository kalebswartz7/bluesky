import asyncio
import pytest
from bluesky.run_engine import RunEngine, RunEngineStateMachine
from bluesky import Msg
from bluesky.examples import det

def test_states():
    assert RunEngineStateMachine.States.states() == ['idle', 'running', 'paused']


def test_verbose(fresh_RE):
    fresh_RE.verbose = True
    fresh_RE.verbose == True
    # Emit all four kinds of document, exercising the logging.
    fresh_RE([Msg('open_run'), Msg('create'), Msg('read', det), Msg('save'),
              Msg('close_run')])


def test_reset(fresh_RE):
    fresh_RE([Msg('open_run'), Msg('pause')])
    assert fresh_RE._run_start_uid != None
    fresh_RE.reset()
    assert fresh_RE._run_start_uid == None


def test_not_idle(fresh_RE):
    fresh_RE([Msg('pause')])
    assert fresh_RE.state == 'paused'
    with pytest.raises(RuntimeError):
        fresh_RE([Msg('null')])
    fresh_RE.resume()
    assert fresh_RE.state == 'idle'
    fresh_RE([Msg('null')])
