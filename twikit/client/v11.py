from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..guest.client import GuestClient
    from .client import Client

    ClientType = Client | GuestClient


class Endpoint:
    GUEST_ACTIVATE = 'https://api.x.com/1.1/guest/activate.json'
    ONBOARDING_SSO_INIT = 'https://api.x.com/1.1/onboarding/sso_init.json'
    ACCOUNT_LOGOUT = 'https://api.x.com/1.1/account/logout.json'
    ONBOARDING_TASK = 'https://api.x.com/1.1/onboarding/task.json'
    SETTINGS = 'https://api.x.com/1.1/account/settings.json'
    UPDATE_PROFILE = 'https://api.x.com/1.1/account/update_profile.json'
    UPDATE_PROFILE_IMAGE = 'https://api.x.com/1.1/account/update_profile_image.json'
    UPDATE_PROFILE_BANNER = 'https://api.x.com/1.1/account/update_profile_banner.json'
    UPLOAD_MEDIA = 'https://upload.x.com/i/media/upload.json'
    UPLOAD_MEDIA_2 = 'https://upload.x.com/i/media/upload2.json'
    CREATE_MEDIA_METADATA = 'https://api.x.com/1.1/media/metadata/create.json'
    CREATE_CARD = 'https://caps.x.com/v2/cards/create.json'
    VOTE = 'https://caps.x.com/v2/capi/passthrough/1'
    REVERSE_GEOCODE = 'https://api.x.com/1.1/geo/reverse_geocode.json'
    SEARCH_GEO = 'https://api.x.com/1.1/geo/search.json'
    GET_PLACE = 'https://api.x.com/1.1/geo/id/{}.json'
    AVAILABLE_TRENDS = 'https://api.x.com/1.1/trends/available.json'
    PLACE_TRENDS = 'https://api.x.com/1.1/trends/place.json'
    FOLLOWERS_LIST = 'https://api.x.com/1.1/followers/list.json'
    FRIENDS_LIST = 'https://api.x.com/1.1/friends/list.json'
    FOLLOWERS_IDS = 'https://api.x.com/1.1/followers/ids.json'
    FRIENDS_IDS = 'https://api.x.com/1.1/friends/ids.json'
    CREATE_FRIENDSHIPS = 'https://x.com/i/api/1.1/friendships/create.json'
    DESTROY_FRIENDSHIPS = 'https://x.com/i/api/1.1/friendships/destroy.json'
    CREATE_BLOCKS = 'https://x.com/i/api/1.1/blocks/create.json'
    DESTROY_BLOCKS = 'https://x.com/i/api/1.1/blocks/destroy.json'
    CREATE_MUTES = 'https://x.com/i/api/1.1/mutes/users/create.json'
    DESTROY_MUTES = 'https://x.com/i/api/1.1/mutes/users/destroy.json'
    DM_NEW = 'https://x.com/i/api/1.1/dm/new2.json'
    DM_INBOX = 'https://x.com/i/api/1.1/dm/inbox_initial_state.json'
    DM_CONVERSATION = 'https://x.com/i/api/1.1/dm/conversation/{}.json'
    CONVERSATION_UPDATE_NAME = 'https://x.com/i/api/1.1/dm/conversation/{}/update_name.json'
    CONVERSATION_MARK_READ = 'https://x.com/i/api/1.1/dm/conversation/{}/mark_read.json'
    CONVERSATION_UPDATE_LAST_SEEN = 'https://x.com/i/api/1.1/dm/update_last_seen_event_id'

    GUIDE = 'https://x.com/i/api/2/guide.json'
    NOTIFICATIONS_ALL = 'https://x.com/i/api/2/notifications/all.json'
    NOTIFICATIONS_VERIFIED = 'https://x.com/i/api/2/notifications/verified.json'
    NOTIFICATIONS_MENTIONS = 'https://x.com/i/api/2/notifications/mentions.json'
    NOTIFICATIONS_LAST_SEEN = 'https://x.com/i/api/2/notifications/all/last_seen_cursor.json'
    BADGE_COUNT = 'https://x.com/i/api/2/badge_count/badge_count.json'

    LIVE_PIPELINE_EVENTS = 'https://api.x.com/live_pipeline/events'
    LIVE_PIPELINE_UPDATE_SUBSCRIPTIONS = 'https://api.x.com/1.1/live_pipeline/update_subscriptions'
    USER_STATE = 'https://api.x.com/help-center/forms/api/prod/user_state.json'


class V11Client:
    def __init__(self, base: ClientType, token) -> None:
        self.base = base
        self._token = token

    async def guest_activate(self):
        headers = self.base._base_headers
        if 'X-Twitter-Active-User' in headers:
            headers.pop('X-Twitter-Active-User')
        if 'X-Twitter-Auth-Type' in headers:
            headers.pop('X-Twitter-Auth-Type')
        return await self.base.post(
            Endpoint.GUEST_ACTIVATE,
            headers=headers,
            data={}
        )

    async def account_logout(self):
        return await self.base.post(
            Endpoint.ACCOUNT_LOGOUT,
            headers=self.base._base_headers
        )

    async def onboarding_task(self, guest_token, token, subtask_inputs, data = None, **kwargs):
        if data is None:
            data = {}
        if token is not None:
            data['flow_token'] = token
        if subtask_inputs is not None:
            data['subtask_inputs'] = subtask_inputs

        headers = {
            'x-guest-token': guest_token,
            'Authorization': 'Bearer ' + self._token
        }

        if self.base._get_csrf_token():
            headers["x-csrf-token"] = self.base._get_csrf_token()
            headers["X-Twitter-Auth-Type"] = "OAuth2Session"

        return await self.base.post(
            Endpoint.ONBOARDING_TASK,
            json=data,
            headers=headers,
            **kwargs
        )

    async def sso_init(self, provider, guest_token):
        headers = self.base._base_headers | {
            'x-guest-token': guest_token
        }
        if 'X-Twitter-Active-User' in headers:
            headers.pop('X-Twitter-Active-User')
        if 'X-Twitter-Auth-Type' in headers:
            headers.pop('X-Twitter-Auth-Type')
        return await self.base.post(
            Endpoint.ONBOARDING_SSO_INIT,
            json={'provider': provider},
            headers=headers
        )

    async def settings(self):
        return await self.base.get(
            Endpoint.SETTINGS,
            headers=self.base._base_headers
        )

    async def upload_media(self, method, is_long_video: bool, *args, **kwargs):
        if is_long_video:
            endpoint = Endpoint.UPLOAD_MEDIA_2
        else:
            endpoint = Endpoint.UPLOAD_MEDIA
        return await self.base.request(method, endpoint, *args, **kwargs)

    async def upload_media_init(self, media_type, total_bytes, media_category, is_long_video: bool):
        params = {
            'command': 'INIT',
            'total_bytes': total_bytes,
            'media_type': media_type
        }
        if media_category is not None:
            params['media_category'] = media_category

        return await self.upload_media(
            'POST',
            is_long_video,
            params=params,
            headers=self.base._base_headers
        )

    async def upload_media_append(self, is_long_video, media_id, segment_index, chunk_stream):
        params = {
            'command': 'APPEND',
            'media_id': media_id,
            'segment_index': segment_index,
        }
        headers = self.base._base_headers
        headers.pop('Content-Type')
        files = {
            'media': (
                'blob',
                chunk_stream,
                'application/octet-stream',
            )
        }
        return await self.upload_media(
            'POST',
            is_long_video,
            params=params,
            headers=headers, files=files
        )

    async def upload_media_finelize(self, is_long_video, media_id):
        params = {
            'command': 'FINALIZE',
            'media_id': media_id,
        }
        return await self.upload_media(
            'POST',
            is_long_video,
            params=params,
            headers=self.base._base_headers,
        )

    async def upload_media_status(self, is_long_video, media_id):
        params = {
            'command': 'STATUS',
            'media_id': media_id,
        }
        return await self.upload_media(
            'GET',
            is_long_video,
            params=params,
            headers=self.base._base_headers,
        )

    async def create_media_metadata(self, media_id, alt_text, sensitive_warning):
        data = {'media_id': media_id}
        if alt_text is not None:
            data['alt_text'] = {'text': alt_text}
        if sensitive_warning is not None:
            data['sensitive_media_warning'] = sensitive_warning
        return await self.base.post(
            Endpoint.CREATE_MEDIA_METADATA,
            json=data,
            headers=self.base._base_headers
        )

    async def create_card(self, choices, duration_minutes):
        card_data = {
            'twitter:card': f'poll{len(choices)}choice_text_only',
            'twitter:api:api:endpoint': '1',
            'twitter:long:duration_minutes': duration_minutes
        }

        for i, choice in enumerate(choices, 1):
            card_data[f'twitter:string:choice{i}_label'] = choice

        data = {'card_data': json.dumps(card_data)}
        headers = self.base._base_headers | {'Content-Type': 'application/x-www-form-urlencoded'}
        return await self.base.post(
            Endpoint.CREATE_CARD,
            data=data,
            headers=headers,
        )

    async def vote(self, selected_choice: str, card_uri: str, tweet_id: str, card_name: str):
        data = {
            'twitter:string:card_uri': card_uri,
            'twitter:long:original_tweet_id': tweet_id,
            'twitter:string:response_card_name': card_name,
            'twitter:string:cards_platform': 'Web-12',
            'twitter:string:selected_choice': selected_choice
        }
        headers = self.base._base_headers | {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        return await self.base.post(
            Endpoint.VOTE,
            data=data,
            headers=headers
        )

    async def reverse_geocode(self, lat, long, accuracy, granularity, max_results):
        params = {
            'lat': lat,
            'long': long,
            'accuracy': accuracy,
            'granularity': granularity,
            'max_results': max_results
        }
        for k, v in tuple(params.items()):
            if v is None:
                params.pop(k)
        return await self.base.get(
            Endpoint.REVERSE_GEOCODE,
            params=params,
            headers=self.base._base_headers
        )

    async def search_geo(self, lat, long, query, ip, granularity, max_results):
        params = {
            'lat': lat,
            'long': long,
            'query': query,
            'ip': ip,
            'granularity': granularity,
            'max_results': max_results
        }
        for k, v in tuple(params.items()):
            if v is None:
                params.pop(k)

        return await self.base.get(
            Endpoint.SEARCH_GEO,
            params=params,
            headers=self.base._base_headers
        )

    async def get_place(self, id):
        return await self.base.get(
            Endpoint.GET_PLACE.format(id),
            headers=self.base._base_headers
        )

    async def create_friendships(self, user_id):
        data = {
            'include_profile_interstitial_type': 1,
            'include_blocking': 1,
            'include_blocked_by': 1,
            'include_followed_by': 1,
            'include_want_retweets': 1,
            'include_mute_edge': 1,
            'include_can_dm': 1,
            'include_can_media_tag': 1,
            'include_ext_is_blue_verified': 1,
            'include_ext_verified_type': 1,
            'include_ext_profile_image_shape': 1,
            'skip_status': 1,
            'user_id': user_id
        }
        headers = self.base._base_headers | {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        return await self.base.post(
            Endpoint.CREATE_FRIENDSHIPS,
            data=data,
            headers=headers
        )

    async def destroy_friendships(self, user_id):
        data = {
            'include_profile_interstitial_type': 1,
            'include_blocking': 1,
            'include_blocked_by': 1,
            'include_followed_by': 1,
            'include_want_retweets': 1,
            'include_mute_edge': 1,
            'include_can_dm': 1,
            'include_can_media_tag': 1,
            'include_ext_is_blue_verified': 1,
            'include_ext_verified_type': 1,
            'include_ext_profile_image_shape': 1,
            'skip_status': 1,
            'user_id': user_id
        }
        headers = self.base._base_headers | {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        return await self.base.post(
            Endpoint.DESTROY_FRIENDSHIPS,
            data=data,
            headers=headers
        )

    async def create_blocks(self, user_id):
        data = {'user_id': user_id}
        headers = self.base._base_headers
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return await self.base.post(
            Endpoint.CREATE_BLOCKS,
            data=data,
            headers=headers
        )

    async def destroy_blocks(self, user_id):
        data = {'user_id': user_id}
        headers = self.base._base_headers
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return await self.base.post(
            Endpoint.DESTROY_BLOCKS,
            data=data,
            headers=headers
        )

    async def create_mutes(self, user_id):
        data = {'user_id': user_id}
        headers = self.base._base_headers
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return await self.base.post(
            Endpoint.CREATE_MUTES,
            data=data,
            headers=headers
        )

    async def destroy_mutes(self, user_id):
        data = {'user_id': user_id}
        headers = self.base._base_headers
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return await self.base.post(
            Endpoint.DESTROY_MUTES,
            data=data,
            headers=headers
        )

    async def guide(self, category, count, additional_request_params):
        params = {
            'count': count,
            'include_page_configuration': True,
            'initial_tab_id': category
        }
        if additional_request_params is not None:
            params |= additional_request_params
        return await self.base.get(
            Endpoint.GUIDE,
            params=params,
            headers=self.base._base_headers
        )

    async def badge_count(self):
        params = {'supports_ntab_urt': 1}
        return await self.base.get(
            Endpoint.BADGE_COUNT,
            params=params,
            headers=self.base._base_headers
        )

    async def available_trends(self):
        return await self.base.get(
            Endpoint.AVAILABLE_TRENDS,
            headers=self.base._base_headers
        )

    async def place_trends(self, woeid):
        return await self.base.get(
            Endpoint.PLACE_TRENDS,
            params={'id': woeid},
            headers=self.base._base_headers
        )

    async def _friendships(self, user_id, screen_name, count, endpoint, cursor):
        params = {'count': count}
        if user_id is not None:
            params['user_id'] = user_id
        elif screen_name is not None:
            params['screen_name'] = screen_name

        if cursor is not None:
            params['cursor'] = cursor

        return await self.base.get(
            endpoint,
            params=params,
            headers=self.base._base_headers
        )

    async def followers_list(self, user_id, screen_name, count, cursor):
        return await self._friendships(user_id, screen_name, count, Endpoint.FOLLOWERS_LIST, cursor)

    async def friends_list(self, user_id, screen_name, count, cursor):
        return await self._friendships(user_id, screen_name, count, Endpoint.FRIENDS_LIST, cursor)

    async def _friendship_ids(self, user_id, screen_name, count, endpoint, cursor):
        params = {'count': count}
        if user_id is not None:
            params['user_id'] = user_id
        elif user_id is not None:
            params['screen_name'] = screen_name

        if cursor is not None:
            params['cursor'] = cursor

        return await self.base.get(
            endpoint,
            params=params,
            headers=self.base._base_headers
        )

    async def followers_ids(self, user_id, screen_name, count, cursor):
        return await self._friendship_ids(user_id, screen_name, count, Endpoint.FOLLOWERS_IDS, cursor)

    async def friends_ids(self, user_id, screen_name, count, cursor):
        return await self._friendship_ids(user_id, screen_name, count, Endpoint.FRIENDS_IDS, cursor)

    async def dm_new(self, conversation_id, text, media_id, reply_to):
        params = {
            'ext': 'mediaColor,altText,mediaStats,highlightedLabel,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl,article',
            'include_ext_alt_text': True,
            'include_ext_limited_action_results': True,
            'include_reply_count': 1,
            'tweet_mode': 'extended',
            'include_ext_views': True,
            'include_groups': True,
            'include_inbox_timelines': True,
            'include_ext_media_color': True,
            'supports_reactions': True,
            'supports_edit': True
        }

        data = {
            'cards_platform': 'Web-12',
            'conversation_id': conversation_id,
            'dm_users': False,
            'include_cards': 1,
            'include_quote_count': True,
            'recipient_ids': False,
            'text': text
        }
        if media_id is not None:
            data['media_id'] = media_id
        if reply_to is not None:
            data['reply_to_dm_id'] = reply_to

        return await self.base.post(
            Endpoint.DM_NEW,
            params=params,
            json=data,
            headers=self.base._base_headers
        )

    async def dm_inbox(self, max_id):
        params = {
            'nsfw_filtering_enabled': False,
            'include_profile_interstitial_type': 1,
            'include_blocking': 1,
            'include_blocked_by': 1,
            'include_followed_by': 1,
            'include_want_retweets': 1,
            'include_mute_edge': 1,
            'include_can_dm': 1,
            'include_can_media_tag': 1,
            'include_ext_is_blue_verified': 1,
            'include_ext_verified_type': 1,
            'include_ext_profile_image_shape': 1,
            'skip_status': 1,
            'dm_secret_conversations_enabled': False,
            'krs_registration_enabled': True,
            'cards_platform': 'Web-12',
            'include_cards': 1,
            'include_ext_alt_text': True,
            'include_ext_limited_action_results': True,
            'include_quote_count': True,
            'include_reply_count': 1,
            'tweet_mode': 'extended',
            'include_ext_views': True,
            'dm_users': True,
            'include_groups': True,
            'include_inbox_timelines': True,
            'include_ext_media_color': True,
            'supports_reactions': True,
            'supports_edit': True,
            'include_ext_edit_control': True,
            'include_ext_business_affiliations_label': True,
            'ext': 'mediaColor,altText,mediaStats,highlightedLabel,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl,article'
        }
        if max_id is not None:
            params['max_id'] = max_id
        return await self.base.get(
            Endpoint.DM_INBOX,
            params=params,
            headers=self.base._base_headers
        )

    async def dm_conversation(self, conversation_id, max_id):
        params = {'context': 'FETCH_DM_CONVERSATION_HISTORY', 'include_conversation_info': True}
        if max_id is not None:
            params['max_id'] = max_id

        return await self.base.get(
            Endpoint.DM_CONVERSATION.format(conversation_id),
            params=params,
            headers=self.base._base_headers
        )

    async def conversation_update_name(self, group_id, name):
        data = {'name': name}
        headers = self.base._base_headers
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return await self.base.post(
            Endpoint.CONVERSATION_UPDATE_NAME.format(group_id),
            data=data,
            headers=headers
        )

    async def conversation_mark_read(self, conversation_id, event_id):
        data = {'conversationId': conversation_id, 'last_read_event_id': event_id}
        headers = self.base._base_headers
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return await self.base.post(
            Endpoint.CONVERSATION_MARK_READ.format(conversation_id),
            data=data,
            headers=headers
        )

    async def conversation_update_last_seen(self, event_id):
        data = {'last_seen_event_id': event_id, 'trusted_last_seen_event_id': event_id}
        headers = self.base._base_headers
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return await self.base.post(
            Endpoint.CONVERSATION_UPDATE_LAST_SEEN,
            data=data,
            headers=headers
        )

    async def _notifications(self, endpoint, count, cursor):
        params = {
            'include_profile_interstitial_type': 1,
            'include_blocking': 1,
            'include_blocked_by': 1,
            'include_followed_by': 1,
            'include_want_retweets': 1,
            'include_mute_edge': 1,
            'include_can_dm': 1,
            'include_can_media_tag': 1,
            'include_ext_is_blue_verified': 1,
            'include_ext_verified_type': 1,
            'include_ext_profile_image_shape': 1,
            'skip_status': 1,
            'cards_platform': 'Web-12',
            'include_cards': 1,
            'include_ext_alt_text': True,
            'include_ext_limited_action_results': True,
            'include_quote_count': True,
            'include_reply_count': 1,
            'tweet_mode': 'extended',
            'include_ext_views': True,
            'include_entities': True,
            'include_user_entities': True,
            'include_ext_media_color': True,
            'include_ext_media_availability': True,
            'include_ext_sensitive_media_warning': True,
            'include_ext_trusted_friends_metadata': True,
            'send_error_codes': True,
            'simple_quoted_tweet': True,
            'count': count,
            'requestContext': 'launch',
            'ext' : 'mediaStats,highlightedLabel,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl,article'
        }
        if cursor is not None:
            params['cursor'] = cursor

        return await self.base.get(
            endpoint,
            params=params,
            headers=self.base._base_headers
        )

    async def notifications_all(self, count, cursor):
        return await self._notifications(Endpoint.NOTIFICATIONS_ALL, count, cursor)

    async def notifications_verified(self, count, cursor):
        return await self._notifications(Endpoint.NOTIFICATIONS_VERIFIED, count, cursor)

    async def notifications_mentions(self, count, cursor):
        return await self._notifications(Endpoint.NOTIFICATIONS_MENTIONS, count, cursor)

    async def notifications_last_seen(self, cursor):
        data = {'cursor': cursor}
        headers = self.base._base_headers
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return await self.base.post(
            Endpoint.NOTIFICATIONS_LAST_SEEN,
            data=data,
            headers=headers
        )

    async def live_pipeline_update_subscriptions(self, session, subscribe, unsubscribe):
        data = {
            'sub_topics': subscribe,
            'unsub_topics': unsubscribe
        }
        headers = self.base._base_headers
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['LivePipeline-Session'] = session
        return await self.base.post(
            Endpoint.LIVE_PIPELINE_UPDATE_SUBSCRIPTIONS, data=data, headers=headers
        )

    async def user_state(self):
        return await self.base.get(
            Endpoint.USER_STATE,
            headers=self.base._base_headers
        )
        
    async def update_profile(self, name, url, location, description):
        params = {}
        if name is not None:
            params['name'] = name
        if url is not None:
            params['url'] = url
        if location is not None:
            params['location'] = location
        if description is not None:
            params['description'] = description

        return await self.base.post(
            Endpoint.UPDATE_PROFILE,
            params=params,
            headers=self.base._base_headers
        )
        
    async def update_profile_image(self, image_base64):
        params = {
            'image': image_base64
        }
        
        return await self.base.post(
            Endpoint.UPDATE_PROFILE_IMAGE,
            params=params,
            headers=self.base._base_headers
        )
        
    async def update_profile_banner(self, image_base64):
        params = {
            'banner': image_base64
        }
        
        return await self.base.post(
            Endpoint.UPDATE_PROFILE_BANNER,
            params=params,
            data=params,
            headers=self.base._base_headers
        )