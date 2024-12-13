from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.request import urlopen
import json

from ..constants import (
    BOOKMARK_FOLDER_TIMELINE_FEATURES,
    COMMUNITY_NOTE_FEATURES,
    COMMUNITY_TWEETS_FEATURES,
    FEATURES,
    TWEET_FEATURES,
    LIST_LATEST_TWEETS_FEATURES,
    JOIN_COMMUNITY_FEATURES,
    LIST_FEATURES,
    NOTE_TWEET_FEATURES,
    SIMILAR_POSTS_FEATURES,
    TWEET_RESULT_BY_REST_ID_FEATURES,
    USER_FEATURES,
    USER_HIGHLIGHTS_TWEETS_FEATURES
)
from ..utils import flatten_params, get_query_id

if TYPE_CHECKING:
    from ..guest.client import GuestClient
    from .client import Client

    ClientType = Client | GuestClient


class Endpoint:
    @staticmethod
    def url(path):
        return 'https://x.com/i/api/graphql/' + path

    SEARCH_TIMELINE = url('H3x0obeAvb20fwqp7wBBjA/SearchTimeline')
    SIMILAR_POSTS = url('EToazR74i0rJyZYalfVEAQ/SimilarPosts')
    CREATE_NOTE_TWEET = url('iCUB42lIfXf9qPKctjE5rQ/CreateNoteTweet')
    CREATE_TWEET = url('sQhC96QH-hw_8TjKE3kW3g/CreateTweet')
    CREATE_SCHEDULED_TWEET = url('LCVzRQGxOaGnOnYH01NQXg/CreateScheduledTweet')
    DELETE_TWEET = url('VaenaVgh5q5ih7kvyVjgtg/DeleteTweet')
    VIEWER_USER_QUERY = url('_nUEOKeLIbspZSgDmgbzxw/ViewerUserQuery')
    USER_BY_SCREEN_NAME = url('NimuplG1OB7Fd2btCLdBOw/UserByScreenName')
    USER_BY_REST_ID = url('tD8zKvQzwY3kdx5yz6YmOw/UserByRestId')
    TWEET_DETAIL = url('GBSfDNBdZPRdJCfYd3mR7Q/TweetDetail')
    TWEET_RESULT_BY_REST_ID = url('Xl5pC_lBk_gcO2ItU39DQw/TweetResultByRestId')
    FETCH_SCHEDULED_TWEETS = url('ITtjAzvlZni2wWXwf295Qg/FetchScheduledTweets')
    DELETE_SCHEDULED_TWEET = url('CTOVqej0JBXAZSwkp1US0g/DeleteScheduledTweet')
    RETWEETERS = url('X-XEqG5qHQSAwmvy00xfyQ/Retweeters')
    FAVORITERS = url('LLkw5EcVutJL6y-2gkz22A/Favoriters')
    FETCH_COMMUNITY_NOTE = url('fKWPPj271aTM-AB9Xp48IA/BirdwatchFetchOneNote')
    USER_TWEETS = url('QWF3SzpHmykQHsQMixG0cg/UserTweets')
    USER_TWEETS_AND_REPLIES = url('vMkJyzx1wdmvOeeNG0n6Wg/UserTweetsAndReplies')
    USER_MEDIA = url('2tLOJWwGuCTytDrGBg8VwQ/UserMedia')
    USER_LIKES = url('IohM3gxQHfvWePH5E3KuNA/Likes')
    USER_HIGHLIGHTS_TWEETS = url('tHFm_XZc_NNi-CfUThwbNw/UserHighlightsTweets')
    HOME_TIMELINE = url('-X_hcgQzmHGl29-UXxz4sw/HomeTimeline')
    HOME_LATEST_TIMELINE = url('U0cdisy7QFIoTfu3-Okw0A/HomeLatestTimeline')
    FAVORITE_TWEET = url('lI07N6Otwv1PhnEgXILM7A/FavoriteTweet')
    UNFAVORITE_TWEET = url('ZYKSe-w7KEslx3JhSIk5LA/UnfavoriteTweet')
    CREATE_RETWEET = url('ojPdsZsimiJrUGLR1sjUtA/CreateRetweet')
    DELETE_RETWEET = url('iQtK4dl5hBmXewYZuEOKVw/DeleteRetweet')
    CREATE_BOOKMARK = url('aoDbu3RHznuiSkQ9aNM67Q/CreateBookmark')
    BOOKMARK_TO_FOLDER = url('4KHZvvNbHNf07bsgnL9gWA/bookmarkTweetToFolder')
    DELETE_BOOKMARK = url('Wlmlj2-xzyS1GN3a6cj-mQ/DeleteBookmark')
    BOOKMARKS = url('qToeLeMs43Q8cr7tRYXmaQ/Bookmarks')
    BOOKMARK_FOLDER_TIMELINE = url('8HoabOvl7jl9IC1Aixj-vg/BookmarkFolderTimeline')
    BOOKMARKS_ALL_DELETE = url('skiACZKC1GDYli-M8RzEPQ/BookmarksAllDelete')
    BOOKMARK_FOLDERS_SLICE = url('i78YDd0Tza-dV4SYs58kRg/BookmarkFoldersSlice')
    EDIT_BOOKMARK_FOLDER = url('a6kPp1cS1Dgbsjhapz1PNw/EditBookmarkFolder')
    DELETE_BOOKMARK_FOLDER = url('2UTTsO-6zs93XqlEUZPsSg/DeleteBookmarkFolder')
    CREATE_BOOKMARK_FOLDER = url('6Xxqpq8TM_CREYiuof_h5w/createBookmarkFolder')
    FOLLOWERS = url('gC_lyAxZOptAMLCJX5UhWw/Followers')
    BLUE_VERIFIED_FOLLOWERS = url('VmIlPJNEDVQ29HfzIhV4mw/BlueVerifiedFollowers')
    FOLLOWERS_YOU_KNOW = url('f2tbuGNjfOE8mNUO5itMew/FollowersYouKnow')
    FOLLOWING = url('2vUj-_Ek-UmBVDNtd8OnQA/Following')
    USER_CREATOR_SUBSCRIPTIONS = url('Wsm5ZTCYtg2eH7mXAXPIgw/UserCreatorSubscriptions')
    USER_DM_REACTION_MUTATION_ADD_MUTATION = url('VyDyV9pC2oZEj6g52hgnhA/useDMReactionMutationAddMutation')
    USER_DM_REACTION_MUTATION_REMOVE_MUTATION = url('bV_Nim3RYHsaJwMkTXJ6ew/useDMReactionMutationRemoveMutation')
    DM_MESSAGE_DELETE_MUTATION = url('BJ6DtxA2llfjnRoRjaiIiw/DMMessageDeleteMutation')
    ADD_PARTICIPANTS_MUTATION = url('oBwyQ0_xVbAQ8FAyG0pCRA/AddParticipantsMutation')
    CREATE_LIST = url('EYg7JZU3A1eJ-wr2eygPHQ/CreateList')
    EDIT_LIST_BANNER = url('t_DsROHldculsB0B9BUAWw/EditListBanner')
    DELETE_LIST_BANNER = url('Y90WuxdWugtMRJhkXTdvzg/DeleteListBanner')
    UPDATE_LIST = url('dIEI1sbSAuZlxhE0ggrezA/UpdateList')
    LIST_ADD_MEMBER = url('lLNsL7mW6gSEQG6rXP7TNw/ListAddMember')
    LIST_REMOVE_MEMBER = url('cvDFkG5WjcXV0Qw5nfe1qQ/ListRemoveMember')
    LIST_MANAGEMENT_PACE_TIMELINE = url('47170qwZCt5aFo9cBwFoNA/ListsManagementPageTimeline')
    LIST_BY_REST_ID = url('9hbYpeVBMq8-yB8slayGWQ/ListByRestId')
    LIST_LATEST_TWEETS_TIMELINE = url('f-F9zCUgaJDQ9ubKsuntiw/ListLatestTweetsTimeline')
    LIST_MEMBERS = url('BQp2IEYkgxuSxqbTAr1e1g/ListMembers')
    LIST_SUBSCRIBERS = url('74wGEkaBxrdoXakWTWMxRQ/ListSubscribers')
    SEARCH_COMMUNITY = url('daVUkhfHn7-Z8llpYVKJSw/CommunitiesSearchQuery')
    COMMUNITY_QUERY = url('lUBKrilodgg9Nikaw3cIiA/CommunityQuery')
    COMMUNITY_MEDIA_TIMELINE = url('Ht5K2ckaZYAOuRFmFfbHig/CommunityMediaTimeline')
    COMMUNITY_TWEETS_TIMELINE = url('mhwSsmub4JZgHcs0dtsjrw/CommunityTweetsTimeline')
    COMMUNITIES_MAIN_PAGE_TIMELINE = url('4-4iuIdaLPpmxKnA3mr2LA/CommunitiesMainPageTimeline')
    JOIN_COMMUNITY = url('xZQLbDwbI585YTG0QIpokw/JoinCommunity')
    LEAVE_COMMUNITY = url('OoS6Kd4-noNLXPZYHtygeA/LeaveCommunity')
    REQUEST_TO_JOIN_COMMUNITY = url('XwWChphD_6g7JnsFus2f2Q/RequestToJoinCommunity')
    MEMBERS_SLICE_TIMELINE_QUERY = url('KDAssJ5lafCy-asH4wm1dw/membersSliceTimeline_Query')
    MODERATORS_SLICE_TIMELINE_QUERY = url('9KI_r8e-tgp3--N5SZYVjg/moderatorsSliceTimeline_Query')
    COMMUNITY_TWEET_SEARCH_MODULE_QUERY = url('5341rmzzvdjqfmPKfoHUBw/CommunityTweetSearchModuleQuery')


class GQLClient:
    def __init__(self, base: ClientType) -> None:
        self.base = base
        with urlopen(
            'https://raw.githubusercontent.com/fa0311/TwitterInternalAPIDocument/refs/heads/master/docs/json/API.json'
        ) as f:
            data = json.load(f)
            for endpoint, value in data['graphql'].items():
                setattr(Endpoint, endpoint, type('obj', (object,), {'url': value['url'], 'features': value['features']}))

    async def gql_get(
        self,
        url: str,
        variables: dict,
        features: dict | None = None,
        headers: dict | None = None,
        extra_params: dict | None = None,
        **kwargs
    ):
        params = {'variables': variables}
        if features is not None:
            params['features'] = features
        if extra_params is not None:
            params |= extra_params
        if headers is None:
            headers = self.base._base_headers
        return await self.base.get(url, params=flatten_params(params), headers=headers, **kwargs)

    async def gql_post(
        self,
        url: str,
        variables: dict,
        features: dict | None = None,
        headers: dict | None = None,
        extra_data: dict | None = None,
        **kwargs
    ):
        data = {'variables': variables, 'queryId': get_query_id(url)}
        if features is not None:
            data['features'] = features
        if extra_data is not None:
            data |= extra_data
        if headers is None:
            headers = self.base._base_headers
        return await self.base.post(url, json=data, headers=headers, **kwargs)

    async def search_timeline(
        self,
        query: str,
        product: str,
        count: int,
        cursor: str | None
    ):
        variables = {
            'rawQuery': query,
            'count': count,
            'querySource': 'typed_query',
            'product': product
        }
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_get(Endpoint.SearchTimeline.url, variables, Endpoint.SearchTimeline.features)

    async def similar_posts(self, tweet_id: str):
        variables = {'tweet_id': tweet_id}
        return await self.gql_get(
            Endpoint.SimilarPosts.url,
            variables,
            Endpoint.SimilarPosts.features
        )

    async def create_tweet(
        self, is_note_tweet, text, media_entities,
        poll_uri, reply_to, attachment_url,
        community_id, share_with_followers,
        richtext_options, edit_tweet_id, limit_mode
    ):
        variables = {
            'tweet_text': text,
            'dark_request': False,
            'media': {
                'media_entities': media_entities,
                'possibly_sensitive': False
            },
            'semantic_annotation_ids': [],
        }

        if poll_uri is not None:
            variables['card_uri'] = poll_uri

        if reply_to is not None:
            variables['reply'] = {
                'in_reply_to_tweet_id': reply_to,
                'exclude_reply_user_ids': []
            }
            variables['disallowed_reply_options'] = None

        if limit_mode is not None:
            variables['conversation_control'] = {'mode': limit_mode}

        if attachment_url is not None:
            variables['attachment_url'] = attachment_url

        if community_id is not None:
            variables['semantic_annotation_ids'] = [{
                'entity_id': community_id,
                'group_id': '8',
                'domain_id': '31'
            }]
            variables['broadcast'] = share_with_followers

        if richtext_options is not None:
            is_note_tweet = True
            variables['richtext_options'] = {
                'richtext_tags': richtext_options
            }
        if edit_tweet_id is not None:
            variables['edit_options'] = {
                'previous_tweet_id': edit_tweet_id
            }

        if is_note_tweet:
            endpoint = Endpoint.CreateNoteTweet.url
            features = Endpoint.CreateNoteTweet.features
        else:
            endpoint = Endpoint.CreateTweet.url
            features = Endpoint.CreateTweet.features
        return await self.gql_post(endpoint, variables, features)

    async def create_scheduled_tweet(self, scheduled_at, text, media_ids) -> str:
        variables = {
            'post_tweet_request': {
            'auto_populate_reply_metadata': False,
            'status': text,
            'exclude_reply_user_ids': [],
            'media_ids': media_ids
            },
            'execute_at': scheduled_at
        }
        return await self.gql_post(Endpoint.CreateScheduledTweet.url, variables)

    async def delete_tweet(self, tweet_id):
        variables = {
            'tweet_id': tweet_id,
            'dark_request': False
        }
        return await self.gql_post(Endpoint.DeleteTweet.url, variables)

    async def viewer_user_query(self):
        variables = {
           "include_profile_info": True,
           "includeEditPerspective": False,
           "includeHasBirdwatchNotes": False,
           "includeTweetImpression": True,
           "includeEditControl": True
        }
        params = {
            "immersive_video_status_linkable_timestamps": False,
            "blue_business_profile_image_shape_enabled": True,
            "graduated_access_invisible_treatment_enabled": True,
            "subscriptions_verification_info_enabled": True,
            "super_follow_exclusive_tweet_notifications_enabled": True,
            "super_follow_badge_privacy_enabled": True,
            "super_follow_user_api_enabled": True
        }
        return await self.gql_get(Endpoint.VIEWER_USER_QUERY, variables, params)

    async def user_by_screen_name(self, screen_name):
        variables = {
            'screen_name': screen_name,
            'withSafetyModeUserFields': False
        }
        params = {
            'fieldToggles': {'withAuxiliaryUserLabels': False}
        }
        return await self.gql_get(Endpoint.UserByScreenName.url, variables, Endpoint.UserByScreenName.features, extra_params=params)

    async def user_by_rest_id(self, user_id):
        variables = {
            'userId': user_id,
            'withSafetyModeUserFields': True
        }
        return await self.gql_get(Endpoint.UserByRestId.url, variables, Endpoint.UserByRestId.features)

    async def tweet_detail(self, tweet_id, cursor):
        variables = {
            'focalTweetId': tweet_id,
            'referrer': 'tweet',
            #'controller_data': '???',
            'with_rux_injections': False,
            'rankingMode': 'Relevance',
            'includePromotedContent': True,
            'withCommunity': True,
            'withQuickPromoteEligibilityTweetFields': True,
            'withBirdwatchNotes': True,
            'withVoice': True
        }
        if cursor is not None:
            variables['cursor'] = cursor
        params = {
            'fieldToggles': {
                'withArticleRichContentState': True,
                'withArticlePlainText': False,
                'withGrokAnalyze': False,
                'withDisallowedReplyControls': False
            }
        }
        return await self.gql_get(Endpoint.TweetDetail.url, variables, Endpoint.TweetDetail.features, extra_params=params)

    async def fetch_scheduled_tweets(self):
        variables = {'ascending': True}
        return await self.gql_get(Endpoint.FetchScheduledTweets.url, variables)

    async def delete_scheduled_tweet(self, tweet_id):
        variables = {'scheduled_tweet_id': tweet_id}
        return await self.gql_post(Endpoint.DeleteScheduledTweet.url, variables)

    async def tweet_engagements(self, tweet_id, count, cursor, endpoint, features):
        variables = {
            'tweetId': tweet_id,
            'count': count,
            'includePromotedContent': True
        }
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_get(endpoint, variables, features)

    async def retweeters(self, tweet_id, count, cursor):
        return await self.tweet_engagements(tweet_id, count, cursor, Endpoint.Retweeters.url, Endpoint.Retweeters.features)

    async def favoriters(self, tweet_id, count, cursor):
        return await self.tweet_engagements(tweet_id, count, cursor, Endpoint.Favoriters.url, Endpoint.Favoriters.features)

    async def bird_watch_one_note(self, note_id):
        variables = {'note_id': note_id}
        return await self.gql_get(Endpoint.BirdwatchFetchOneNote.url, variables, Endpoint.BirdwatchFetchOneNote.features)

    async def _get_user_tweets(self, user_id, count, cursor, endpoint, features):
        variables = {
            'userId': user_id,
            'count': count,
            'includePromotedContent': True,
            'withQuickPromoteEligibilityTweetFields': True,
            'withVoice': True,
            'withV2Timeline': True
        }
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_get(endpoint, variables, features)

    async def user_tweets(self, user_id, count, cursor):
        return await self._get_user_tweets(user_id, count, cursor, Endpoint.UserTweets.url, Endpoint.UserTweets.features)

    async def user_tweets_and_replies(self, user_id, count, cursor):
        return await self._get_user_tweets(user_id, count, cursor, Endpoint.UserTweetsAndReplies.url, Endpoint.UserTweetsAndReplies.features)

    async def user_media(self, user_id, count, cursor):
        return await self._get_user_tweets(user_id, count, cursor, Endpoint.UserMedia.url, Endpoint.UserMedia.features)

    async def user_likes(self, user_id, count, cursor):
        return await self._get_user_tweets(user_id, count, cursor, Endpoint.Likes.url, Endpoint.Likes.features)

    async def user_highlights_tweets(self, user_id, count, cursor):
        variables = {
            'userId': user_id,
            'count': count,
            'includePromotedContent': True,
            'withVoice': True
        }
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_get(
            Endpoint.UserHighlightsTweets.url,
            variables,
            Endpoint.UserHighlightsTweets.features,
            self.base._base_headers
        )

    async def home_timeline(self, count, seen_tweet_ids, cursor):
        variables = {
            'count': count,
            'includePromotedContent': True,
            'latestControlAvailable': True,
            'requestContext': 'launch',
            'withCommunity': True,
            'seenTweetIds': seen_tweet_ids or []
        }
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_post(Endpoint.HomeTimeline.url, variables, Endpoint.HomeTimeline.features)

    async def home_latest_timeline(self, count, seen_tweet_ids, cursor):
        variables = {
            'count': count,
            'includePromotedContent': True,
            'latestControlAvailable': True,
            'requestContext': 'launch',
            'withCommunity': True,
            'seenTweetIds': seen_tweet_ids or []
        }
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_post(Endpoint.HomeLatestTimeline.url, variables, Endpoint.HomeLatestTimeline.features)

    async def favorite_tweet(self, tweet_id):
        variables = {'tweet_id': tweet_id}
        return await self.gql_post(Endpoint.FavoriteTweet.url, variables)

    async def unfavorite_tweet(self, tweet_id):
        variables = {'tweet_id': tweet_id}
        return await self.gql_post(Endpoint.UnfavoriteTweet.url, variables)

    async def retweet(self, tweet_id):
        variables = {'tweet_id': tweet_id, 'dark_request': False}
        return await self.gql_post(Endpoint.CreateRetweet.url, variables)

    async def delete_retweet(self, tweet_id):
        variables = {'source_tweet_id': tweet_id,'dark_request': False}
        return await self.gql_post(Endpoint.DeleteRetweet.url, variables)

    async def create_bookmark(self, tweet_id):
        variables = {'tweet_id': tweet_id}
        return await self.gql_post(Endpoint.CreateBookmark.url, variables)

    async def bookmark_tweet_to_folder(self, tweet_id, folder_id):
        variables = {
            'tweet_id': tweet_id,
            'bookmark_collection_id': folder_id
        }
        return await self.gql_post(Endpoint.bookmarkTweetToFolder.url, variables)

    async def delete_bookmark(self, tweet_id):
        variables = {'tweet_id': tweet_id}
        return await self.gql_post(Endpoint.DeleteBookmark.url, variables)

    async def bookmarks(self, count, cursor):
        variables = {
            'count': count,
            'includePromotedContent': True
        }
        features = FEATURES | {
            'graphql_timeline_v2_bookmark_timeline': True
        }
        if cursor is not None:
            variables['cursor'] = cursor
        params = flatten_params({
            'variables': variables,
            'features': features
        })
        return await self.base.get(
            Endpoint.BOOKMARKS,
            params=params,
            headers=self.base._base_headers
        )

    async def bookmark_folder_timeline(self, count, cursor, folder_id):
        variables = {
            'count': count,
            'includePromotedContent': True,
            'bookmark_collection_id': folder_id
        }
        variables['bookmark_collection_id'] = folder_id
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_get(Endpoint.BOOKMARK_FOLDER_TIMELINE, variables, BOOKMARK_FOLDER_TIMELINE_FEATURES)

    async def delete_all_bookmarks(self):
        return await self.gql_post(Endpoint.BOOKMARKS_ALL_DELETE, {})

    async def bookmark_folders_slice(self, cursor):
        variables = {}
        if cursor is not None:
            variables['cursor'] = cursor
        variables = {'variables': variables}
        return await self.gql_get(Endpoint.BOOKMARK_FOLDERS_SLICE, variables)

    async def edit_bookmark_folder(self, folder_id, name):
        variables = {
            'bookmark_collection_id': folder_id,
            'name': name
        }
        return await self.gql_post(Endpoint.EDIT_BOOKMARK_FOLDER, variables)

    async def delete_bookmark_folder(self, folder_id):
        variables = {'bookmark_collection_id': folder_id}
        return await self.gql_post(Endpoint.DELETE_BOOKMARK_FOLDER, variables)

    async def create_bookmark_folder(self, name):
        variables = {'name': name}
        return await self.gql_post(Endpoint.CREATE_BOOKMARK_FOLDER, variables)

    async def _friendships(self, user_id, count, endpoint, cursor, features):
        variables = {
            'userId': user_id,
            'count': count,
            'includePromotedContent': False
        }
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_get(endpoint, variables, features)

    async def followers(self, user_id, count, cursor):
        return await self._friendships(user_id, count, Endpoint.Followers.url, cursor, Endpoint.Followers.features)

    async def blue_verified_followers(self, user_id, count, cursor):
        return await self._friendships(user_id, count, Endpoint.BlueVerifiedFollowers.url, cursor, Endpoint.BlueVerifiedFollowers.features)

    async def followers_you_know(self, user_id, count, cursor):
        return await self._friendships(user_id, count, Endpoint.FollowersYouKnow.url, cursor, Endpoint.FollowersYouKnow.features)

    async def following(self, user_id, count, cursor):
        return await self._friendships(user_id, count, Endpoint.Following.url, cursor, Endpoint.Following.features)

    async def user_creator_subscriptions(self, user_id, count, cursor):
        return await self._friendships(user_id, count, Endpoint.UserCreatorSubscriptions.url, cursor, Endpoint.UserCreatorSubscriptions.features)

    async def user_dm_reaction_mutation_add_mutation(self, message_id, conversation_id, emoji):
        variables = {
            'messageId': message_id,
            'conversationId': conversation_id,
            'reactionTypes': ['Emoji'],
            'emojiReactions': [emoji]
        }
        return await self.gql_post(Endpoint.USER_DM_REACTION_MUTATION_ADD_MUTATION, variables)

    async def user_dm_reaction_mutation_remove_mutation(self, message_id, conversation_id, emoji):
        variables = {
            'conversationId': conversation_id,
            'messageId': message_id,
            'reactionTypes': ['Emoji'],
            'emojiReactions': [emoji]
        }
        return await self.gql_post(Endpoint.USER_DM_REACTION_MUTATION_REMOVE_MUTATION, variables)

    async def dm_message_delete_mutation(self, message_id):
        variables = {'messageId': message_id}
        return await self.gql_post(Endpoint.DM_MESSAGE_DELETE_MUTATION, variables)

    async def add_participants_mutation(self, group_id, user_ids):
        variables = {
            'addedParticipants': user_ids,
            'conversationId': group_id
        }
        return await self.gql_post(Endpoint.ADD_PARTICIPANTS_MUTATION, variables)

    async def create_list(self, name, description, is_private):
        variables = {
            'isPrivate': is_private,
            'name': name,
            'description': description
        }
        return await self.gql_post(Endpoint.CREATE_LIST, variables, LIST_FEATURES)

    async def edit_list_banner(self, list_id, media_id):
        variables = {
            'listId': list_id,
            'mediaId': media_id
        }
        return await self.gql_post(Endpoint.EDIT_LIST_BANNER, variables, LIST_FEATURES)

    async def delete_list_banner(self, list_id):
        variables = {'listId': list_id}
        return await self.gql_post(Endpoint.DELETE_LIST_BANNER, variables, LIST_FEATURES)

    async def update_list(self, list_id, name, description, is_private):
        variables = {'listId': list_id}
        if name is not None:
            variables['name'] = name
        if description is not None:
            variables['description'] = description
        if is_private is not None:
            variables['isPrivate'] = is_private
        return await self.gql_post(Endpoint.UPDATE_LIST, variables, LIST_FEATURES)

    async def list_add_member(self, list_id, user_id):
        variables = {
            'listId': list_id,
            'userId': user_id
        }
        return await self.gql_post(Endpoint.LIST_ADD_MEMBER, variables, LIST_FEATURES)

    async def list_remove_member(self, list_id, user_id):
        variables = {
            'listId': list_id,
            'userId': user_id
        }
        return await self.gql_post(Endpoint.LIST_REMOVE_MEMBER, variables, LIST_FEATURES)

    async def list_management_pace_timeline(self, count, cursor):
        variables = {'count': count}
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_get(Endpoint.LIST_MANAGEMENT_PACE_TIMELINE, variables, FEATURES)

    async def list_by_rest_id(self, list_id):
        variables = {'listId': list_id}
        return await self.gql_get(Endpoint.LIST_BY_REST_ID, variables, LIST_FEATURES)

    async def list_latest_tweets_timeline(self, list_id, count, cursor):
        variables = {'listId': list_id, 'count': count}
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_get(Endpoint.ListLatestTweetsTimeline.url, variables, Endpoint.ListLatestTweetsTimeline.features)

    async def _list_users(self, endpoint, list_id, count, cursor, features):
        variables = {'listId': list_id, 'count': count}
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_get(endpoint, variables, features)

    async def list_members(self, list_id, count, cursor):
        return await self._list_users(Endpoint.ListMembers.url, list_id, count, cursor,Endpoint.ListMembers.features)

    async def list_subscribers(self, list_id, count, cursor):
        return await self._list_users(Endpoint.ListSubscribers.url, list_id, count, cursor, Endpoint.ListSubscribers.features)

    async def search_community(self, query, cursor):
        variables = {'query': query}
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_get(Endpoint.SEARCH_COMMUNITY, variables)

    async def community_query(self, community_id):
        variables = {'communityId': community_id}
        features = {
            'c9s_list_members_action_api_enabled': False,
            'c9s_superc9s_indication_enabled': False
        }
        return await self.gql_get(Endpoint.COMMUNITY_QUERY, variables, features)

    async def community_media_timeline(self, community_id, count, cursor):
        variables = {
            'communityId': community_id,
            'count': count,
            'withCommunity': True
        }
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_get(Endpoint.COMMUNITY_MEDIA_TIMELINE, variables, COMMUNITY_TWEETS_FEATURES)

    async def community_tweets_timeline(self, community_id, ranking_mode, count, cursor):
        variables = {
            'communityId': community_id,
            'count': count,
            'withCommunity': True,
            'rankingMode': ranking_mode
        }
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_get(Endpoint.COMMUNITY_TWEETS_TIMELINE, variables, COMMUNITY_TWEETS_FEATURES)

    async def communities_main_page_timeline(self, count, cursor):
        variables = {
            'count': count,
            'withCommunity': True
        }
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_get(Endpoint.COMMUNITIES_MAIN_PAGE_TIMELINE, variables, COMMUNITY_TWEETS_FEATURES)

    async def join_community(self, community_id):
        variables = {'communityId': community_id}
        return await self.gql_post(Endpoint.JOIN_COMMUNITY, variables, JOIN_COMMUNITY_FEATURES)

    async def leave_community(self, community_id):
        variables = {'communityId': community_id}
        return await self.gql_post(Endpoint.LEAVE_COMMUNITY, variables, JOIN_COMMUNITY_FEATURES)

    async def request_to_join_community(self, community_id, answer):
        variables = {
            'communityId': community_id,
            'answer': '' if answer is None else answer
        }
        return await self.gql_post(Endpoint.REQUEST_TO_JOIN_COMMUNITY, variables, JOIN_COMMUNITY_FEATURES)

    async def _get_community_users(self, endpoint, community_id, count, cursor):
        variables = {'communityId': community_id, 'count': count}
        features = {'responsive_web_graphql_timeline_navigation_enabled': True}
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_get(endpoint, variables, features)

    async def members_slice_timeline_query(self, community_id, count, cursor):
        return await self._get_community_users(Endpoint.MEMBERS_SLICE_TIMELINE_QUERY, community_id, count, cursor)

    async def moderators_slice_timeline_query(self, community_id, count, cursor):
        return await self._get_community_users(Endpoint.MODERATORS_SLICE_TIMELINE_QUERY, community_id, count, cursor)

    async def community_tweet_search_module_query(self, community_id, query, count, cursor):
        variables = {
            'count': count,
            'query': query,
            'communityId': community_id,
            'includePromotedContent': False,
            'withBirdwatchNotes': True,
            'withVoice': False,
            'isListMemberTargetUserId': '0',
            'withCommunity': False,
            'withSafetyModeUserFields': True
        }
        if cursor is not None:
            variables['cursor'] = cursor
        return await self.gql_get(Endpoint.COMMUNITY_TWEET_SEARCH_MODULE_QUERY, variables, COMMUNITY_TWEETS_FEATURES)

    ####################
    # For guest client
    ####################

    async def tweet_result_by_rest_id(self, tweet_id):
        variables = {
            'tweetId': tweet_id,
            'withCommunity': False,
            'includePromotedContent': False,
            'withVoice': False
        }
        params = {
            'fieldToggles': {
                'withArticleRichContentState': True,
                'withArticlePlainText': False,
                'withGrokAnalyze': False
            }
        }
        return await self.gql_get(
            Endpoint.TweetResultByRestId.url, variables, Endpoint.TweetResultByRestId.features, extra_params=params
        )
