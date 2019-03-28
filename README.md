PyOxidized
================
A basic Python wrapper for the Oxidized REST API. Full API documentation can be found at the [Oxidized Github repo](https://github.com/ytti/oxidized/blob/1ad63fb18c66e9bd0f64d3d413268feeddd9af7c/README.md).

## Getting Started

### Authentication (Optional)
The client supports basic HTTP authentication for environments where a reverse-proxy (nginx/Apache) was set up in front of Oxidized. Example setup for this can be found on [PacketPushers](https://packetpushers.net/install-oxidized-network-configuration-backup/).

### Example
```
import pyoxidized

host = "http://<oxidized-server>"

# With authentication
oxi = pyoxidized.OxidizedApi(host, username, password)

# Without authentication
oxi = pyoxidized.OxidizedApi(host)

nodes = oxi.get_nodes()
device = nodes[0]
config = oxi.fetch_config(device)
```

## To-Do

- Unit tests
- Diff support
- Show blob of a version