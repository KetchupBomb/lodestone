# FFXVI API for [Lodestone](https://na.finalfantasyxiv.com/lodestone/worldstatus/)

---

A simple Python library for getting server status for FFXIV across its regions, datacenters, and worlds.

## tl;dr

Use it as a library:

```python
>>> import lodestone
>>> lodestone.status("Aegis")
{'Aegis': 'Online (Standard)'}
```

Or use it as a CLI:

```shell
$ ./lodestone.py "elemental" | jq .
{
	"Elemental":{
		"Aegis":"Online (Standard)",
		"Atomos":"Online (Standard)",
		"Carbuncle":"Online (Standard)",
		"Garuda":"Online (Standard)",
		"Gungnir":"Online (Standard)",
		"Kujata":"Online (Standard)",
		"Ramuh":"Online (Standard)",
		"Tonberry":"Online (Congested)",
		"Typhon":"Online (Standard)",
		"Unicorn":"Online (Standard)"
	}
}
```

> Note the case-insensitive query.

Or from the Docker image:

```shell
$ docker run --rm ketchupbomb/lodestone "japan" | jq .
{
	"Japan Data Center":{
		"Elemental":{
			"Aegis":"Online (Standard)",
			"Atomos":"Online (Standard)",
			"Carbuncle":"Online (Standard)",
			"Garuda":"Online (Standard)",
			"Gungnir":"Online (Standard)",
			"Kujata":"Online (Standard)",
			"Ramuh":"Online (Standard)",
			"Tonberry":"Online (Congested)",
			"Typhon":"Online (Standard)",
			"Unicorn":"Online (Standard)"
		},
		"Gaia":{
			"Alexander":"Online (Standard)",
			"Bahamut":"Online (Standard)",
			"Durandal":"Online (Standard)",
			"Fenrir":"Online (Standard)",
			"Ifrit":"Online (Standard)",
			"Ridill":"Online (Standard)",
			"Tiamat":"Online (Standard)",
			"Ultima":"Online (Standard)",
			"Valefor":"Online (Standard)",
			"Yojimbo":"Online (Preferred)",
			"Zeromus":"Online (Preferred)"
		},
		"Mana":{
			"Anima":"Online (Standard)",
			"Asura":"Online (Standard)",
			"Belias":"Online (Standard)",
			"Chocobo":"Online (Standard)",
			"Hades":"Online (Standard)",
			"Ixion":"Online (Standard)",
			"Mandragora":"Online (Standard)",
			"Masamune":"Online (Standard)",
			"Pandaemonium":"Online (Standard)",
			"Shinryu":"Online (Standard)",
			"Titan":"Online (Standard)"
		}
	}
}
```

> Note the partial match query.

Provide no argument for the entire status map.

---

## Gotchas

This module breaks under certain circumstances:

1. If Lodestone is down (typically during upgrades and maintenance), and returns an HTTP 500.
1. If the source HTML structure changes (typically on major version releases).

## Requirements

* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) ([`beautifulsoup4`](https://pypi.org/project/beautifulsoup4/))
* [Requests](http://python-requests.org/) ([`requests`](https://pypi.org/project/requests/))
