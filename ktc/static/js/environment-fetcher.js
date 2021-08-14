// environment-fetcher.js
var environmentFetcher;

environmentFetcher = {
    fetchEnvironments: function () {
        return ['aquatic', 'arctic', 'cave', 'coast', 'desert', 'dungeon', 'forest',
            'grassland', 'mountain', 'planar', 'ruins', 'swamp', 'underground', 'urban']
    }
};

module.exports = environmentFetcher;