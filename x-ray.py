from aws_xray_sdk.core import xray_recorder

xray_recorder.configure(
    sampling=False,
    context_missing='LOG_ERROR',
    plugins='ECSPlugin',
    daemon_address='0.0.0.0:3000'
)