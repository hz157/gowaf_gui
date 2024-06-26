from enum import Enum


class HTTP(object):
    HTTP_100_CONTINUE = 100                            # 继续
    HTTP_101_SWITCHING_PROTOCOLS = 101                 # 交换协议
    HTTP_200_OK = 200                                  # 查询请求成功
    HTTP_201_CREATED = 201                             # 创建成功
    HTTP_202_ACCEPTED = 202                            # 接受
    HTTP_203_NON_AUTHORITATIVE_INFORMATION = 203       # 非权威的信息
    HTTP_204_NO_CONTENT = 204                          # 没有内容
    HTTP_205_RESET_CONTENT = 205                       # 重置内容
    HTTP_206_PARTIAL_CONTENT = 206                     # 部分内容
    HTTP_207_MULTI_STATUS = 207                        # 多状态
    HTTP_300_MULTIPLE_CHOICES = 300                    # 多个选择
    HTTP_301_MOVED_PERMANENTLY = 301                   # 永久重定向
    HTTP_302_FOUND = 302                               # 发现
    HTTP_303_SEE_OTHER = 303                           # 重定向到其他
    HTTP_304_NOT_MODIFIED = 304                        # 未修改
    HTTP_305_USE_PROXY = 305                           # 使用代理
    HTTP_306_RESERVED = 306                            # 未使用
    HTTP_307_TEMPORARY_REDIRECT = 307                  # 临时重定向
    HTTP_400_BAD_REQUEST = 400                         # 错误的请求
    HTTP_401_UNAUTHORIZED = 401                        # 未经授权
    HTTP_402_PAYMENT_REQUIRED = 402                    # 需要授权
    HTTP_403_FORBIDDEN = 403                           # 禁止访问
    HTTP_404_NOT_FOUND = 404                           # 没有找到
    HTTP_405_METHOD_NOT_ALLOWED = 405                  # 方法不允许
    HTTP_406_NOT_ACCEPTABLE = 406                      # 不可接受
    HTTP_407_PROXY_AUTHENTICATION_REQUIRED = 407       # 代理省份验证
    HTTP_408_REQUEST_TIMEOUT = 408                     # 请求超时
    HTTP_409_CONFLICT = 409                            # 资源冲突
    HTTP_410_GONE = 410                                # 资源存在但是不可用了
    HTTP_411_LENGTH_REQUIRED = 411                     # 没有定义content-length
    HTTP_412_PRECONDITION_FAILED = 412                 # 前提条件失败
    HTTP_413_REQUEST_ENTITY_TOO_LARGE = 413            # 请求包太大
    HTTP_414_REQUEST_URI_TOO_LONG = 414                # 请求url太长
    HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415              # 不支持的媒体类型
    HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE = 416     # 请求范围不足
    HTTP_417_EXPECTATION_FAILED = 417                  # 预期失败
    HTTP_422_UNPROCESSABLE_ENTITY = 422                # 不可加工
    HTTP_423_LOCKED = 423                              # 被锁定
    HTTP_424_FAILED_DEPENDENCY = 424                   # 失败的依赖
    HTTP_425_TOO_EARLY = 425                           # 言之过早
    HTTP_428_PRECONDITION_REQUIRED = 428               # 先决条件要求
    HTTP_429_TOO_MANY_REQUESTS = 429                   # 请求太多
    HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE = 431     # 请求头字段太大
    HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS = 451       # 由于法律原因无法使用
    HTTP_500_INTERNAL_SERVER_ERROR = 500               # 服务器错误
    HTTP_501_NOT_IMPLEMENTED = 501                     # 没有实现
    HTTP_502_BAD_GATEWAY = 502                         # 网关错误
    HTTP_503_SERVICE_UNAVAILABLE = 503                 # 服务不可用
    HTTP_504_GATEWAY_TIMEOUT = 504                     # 网关超时
    HTTP_505_HTTP_VERSION_NOT_SUPPORTED = 505          # HTTP协议版本不支持
    HTTP_507_INSUFFICIENT_STORAGE = 507                # 存储不足
    HTTP_511_NETWORK_AUTHENTICATION_REQUIRED = 511     # 网络身份验证要求


class STATUS_CODE(object):
    TOKEN_0_OK = 0                                     # 
    TOKEN_F1_NULL = -1                                   # 
    SERVER_2_ERROR = 2
    TOKEN_50008_ILLEGAL = 50008                        # 无效Token
    TOKEN_50012_LOGOUT = 50012                         # 其他客户端退出
    TOKEN_50014_EXPIRED = 50014                        # Token过期
    