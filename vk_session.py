import vk_api
import conffig

vk_session = vk_api.VkApi(conffig.vk_login, conffig.vk_password)
vk_session.auth()

tools = vk_api.VkTools(vk_session)