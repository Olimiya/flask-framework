
import logging
import flask_jwt_extended

# 1. 完善一键取消授权的鉴权接口。目前已完成一键取消授权的效果。
# 其中原理是使用Monkey Patch，修改verify_jwt和jwt_required的接口，添加optional = true。
# 2. 要求该更改先于其他代码的实现，因此在flask_app的top-level中引入flask_oidc_adapter模块


logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


# Use for test
oidc_auth = False

# 实现一键取消鉴权的接口，基于Monkey Patch原理
# author: lijunhui
# date:   2023/5/12 14:30
original_verify_jwt_in_request = flask_jwt_extended.verify_jwt_in_request


def optional_verify_jwt_in_request(fresh=False, refresh=False, locations=None):
    return original_verify_jwt_in_request(optional=True, fresh=fresh, refresh=refresh, locations=locations)


original_jwt_required = flask_jwt_extended.jwt_required


def optional_jwt_required(fresh=False, refresh=False, locations=None):
    return original_jwt_required(optional=True, fresh=fresh, refresh=refresh, locations=locations)


if not oidc_auth:
    logger.warning("unauth now")
    verify_jwt_in_request = optional_verify_jwt_in_request
    flask_jwt_extended.verify_jwt_in_request = optional_verify_jwt_in_request
    jwt_required = optional_jwt_required
    flask_jwt_extended.jwt_required = optional_jwt_required
