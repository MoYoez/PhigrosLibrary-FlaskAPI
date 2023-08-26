## Phigros Flask API Reference

### Based On [PhigrosLibrary](https://github.com/7aGiven/PhigrosLibrary)

Just Like Phigros Unlimited API, due to it's unstable,so I write this.

### API List

- [x] /api/phi/bests

**Get Users Best, support Overflow songs, you can delete this limit.**

> args: Session | overflow (max:20) | songinfo Optional(bool) (Default:False)

```
{
    "status": true,
    "content": {
        "phi": true,
        "bests": [
            {
                "score": 1000000,
                "acc": 100.0,
                "level": "IN",
                "fc": true,
                "songId": "Adastraperaspera.RabbitHouse",
                "songname": "Ad astra per aspera",
                "difficulty": 15.8,
                "rks": 15.8
            },
            {
                "score": 972338,
                "acc": 99.57353210449219,
                "level": "AT",
                "fc": false,
                "songId": "Stasis.Maozon",
                "songname": "Stasis",
                "difficulty": 16.4,
                "rks": 16.090625251373435
            },
            {
                "score": 975114,
                "acc": 99.28541564941406,
                "level": "AT",
                "fc": false,
                "songId": "DESTRUCTION321.Normal1zervsBrokenNerdz",
                "songname": "DESTRUCTION 3,2,1",
                "difficulty": 16.6,
                "rks": 16.076981457484795
            }
            ...
        ],
        "PlayerID": "压压鸭ya",
        "ChallengeModeRank": 445,
        "RankingScore": 15.800082206726074
    }
}


```

- [x] /api/phi/best

**Check User's best Songs.**

> args: songid | Session | diff: Optional(Default "IN") | songinfo Optional(bool) (Default:False)

- tips: songid just like "DESTRUCTION321.Normal1zervsBrokenNerdz" || diff just like "EZ" "AT" 

```
{
    "status": true,
    "content": {
        "record": {
            "score": 999383,
            "acc": 99.93145751953125,
            "level": "IN",
            "fc": true,
            "songId": "DESTRUCTION321.Normal1zervsBrokenNerdz",
            "songname": "DESTRUCTION 3,2,1",
            "difficulty": 15.9,
            "rks": 15.851600202364502
        },
        "PlayerID": "压压鸭ya",
        "ChallengeModeRank": 445,
        "RankingScore": 15.800082206726074
    }
}

```

- [x] /api/phi/info

**User's Status, no others**

> args: session

```
{
    "status": true,
    "Content": {
        "PlayerID": "MoeMagicMango",
        "ChallengeModeRank": 245,
        "RankingScore": 13.175806999206543
    }
}
```

- [x] /api/phi/rand

> songinfo Optional(bool) (Default:False)

```
{
    "status": true,
    "content": {
        "songid": "BetterGraphicAnimation.ルゼ",
        "songname": "Better Graphic Animation",
        "composer": "ルゼ",
        "level": "HD",
        "rating": 11.7
    }
}
```

- [x] /api/phi/song

> args: songid

```
{
    "status": true,
    "content": {
        "songid": "BetterGraphicAnimation.ルゼ",
        "info": {
            "songname": "Better Graphic Animation",
            "composer": "ルゼ",
            "illustrator": "A-Zero Project",
            "chartDetail": {
                "EZ": {
                    "rating": 6.5,
                    "charter": "NerSAN"
                },
                "HD": {
                    "rating": 11.7,
                    "charter": "NerSAN"
                },
                "In": {
                    "rating": 15.3,
                    "charter": "縱連打の信者☆無極"
                },
                "level_list": [
                    6.5,
                    11.7,
                    15.3
                ]
            }
        }
    }
}
```

...


## License

AGPL-3.0 License

