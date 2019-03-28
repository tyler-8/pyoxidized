import logging
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

RELOAD = "/reload"
NODES = "/nodes"
GROUP_NODES = NODES + "/group/"
FETCH = "/node/fetch/"
FRONT_Q = "/node/next/"
VERSIONS = "/node/version"


class OxidizedApi:
    """
    An Oxidized API Client.
    """

    def __init__(self, host, username, password, verify=True):
        self.host = host
        self.session = requests.Session()
        self.session.verify = verify
        self.session.headers["Content-Type"] = "application/json"

        if username and password:
            self.session.auth = (username, password)

    def get_nodes(self, group=None):
        """
        Restful API to show list of nodes
        (GET /nodes)
        """

        if group:
            url = self.host + GROUP_NODES + group
        else:
            url = self.host + NODES

        params = {"format": "json"}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        nodes = response.json()
        logger.info("Retrieved %s nodes.", len(nodes))
        return nodes

    def reload_nodes(self):
        """
        Restful API to reload list of nodes
        (GET /reload)
        """

        response = self.session.get(self.host + RELOAD)
        response.raise_for_status()
        return response.text

    def get_groups(self):
        """
        Returns list of device groups in oxidized.
        """
        groups = list(set(row["group"] for row in self.get_nodes()))
        return groups

    def get_group_nodes(self, group=None):
        """
        Restful API to show list of nodes for group
        (GET /nodes/group/[GROUP])
        """
        if group is None:
            logger.warning("No group provided, getting all nodes.")
        return self.get_nodes(group=group)

    def fetch_config(self, node):
        """
        Restful API to fetch configurations
        (/node/fetch/[NODE] or /node/fetch/group/[NODE])
        """

        if isinstance(node, dict):
            full_name = node.get("full_name")
        elif isinstance(node, str):
            full_name = node
        else:
            raise TypeError("Must be `group/node` str or oxidized node entry.")

        if not full_name:
            raise Exception(
                "`full_name` key should be present from oxidized node entry."
            )

        response = self.session.get(self.host + FETCH + full_name)
        response.raise_for_status()
        return response.text

    def head_of_queue(self, node):
        """
        Restful API to a move node immediately to head-of-queue
        (GET/POST /node/next/[NODE])
        """
        url = self.host + FRONT_Q + node
        params = {"format": "json"}
        response = self.session.get(url, params=params, allow_redirects=False)
        response.raise_for_status()
        if response.status_code == 302:
            logger.info("Pushed %s to the head of the fetch queue.", node)
            return True
        else:
            logger.warn(
                "Head of queue failed for %s. Received HTTP Status: %s",
                node,
                response.status_code,
            )
            return False

    def list_node_versions(self, node):
        """
        Restful API to show list of version for a node and diffs
        (/node/version?node_full=[NODE])
        """
        url = self.host + VERSIONS
        params = {"node_full": node, "format": "json"}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        versions = response.json()
        logger.info("%s has %s versions", node, len(versions))
        return versions
