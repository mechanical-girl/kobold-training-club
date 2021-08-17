// monster-finder-spec.js
/* jslint node: true */
/* global describe, it, expect */

'use strict';
var findMonsters = require('../ktc/static/js/monster-finder.js');

/*
describe('#monsterFinders.monsterFinders', function () {
    it('should contact the api endpoint /api/monsters and pass back the response', function () {
        var expected = [{ 'alignment': 'neutral good', 'cr': '1/4', 'name': 'Aarakocra', 'size': 'Medium', 'source': 'Monster Manual: 12, Princes of the Apocalypse Online Supplement v1.0: 6', 'type': 'Humanoid' }, { 'alignment': 'neutral good', 'cr': '3', 'name': 'Aarakocra Captain', 'size': 'Medium', 'source': 'Monster Module: 3', 'type': 'Humanoid' }, { 'alignment': 'neutral good', 'cr': '8', 'name': 'Aarakocra Priest of Aerdrie', 'size': 'Medium', 'source': 'Monster Module: 4', 'type': 'Humanoid' }, { 'alignment': 'neutral good', 'cr': '1/2', 'name': 'Aarakocra Sharpshooter', 'size': 'Medium', 'source': 'Monster Module: 3', 'type': 'Humanoid' }, { 'alignment': 'chaotic evil', 'cr': '4', 'name': 'Aaztar-Ghola', 'size': 'Medium', 'source': 'Fifth Edition Foes: 5', 'type': 'Humanoid' }, { 'alignment': 'any', 'cr': '9', 'name': 'Abjurer', 'size': 'Medium', 'source': "Volo's Guide to Monsters: 209", 'type': 'Humanoid' }, { 'alignment': 'lawful evil', 'cr': '10', 'name': 'Aboleth', 'size': 'Large', 'source': 'Monster Manual: 13, Princes of the Apocalypse Online Supplement v1.0: 6', 'type': 'Aberration' }, { 'alignment': 'lawful evil', 'cr': '16', 'name': 'Aboleth Sovereign', 'size': 'Huge', 'source': 'Monster Module: 5', 'type': 'Aberration' }, { 'alignment': 'neutral evil', 'cr': '11', 'name': 'Abominable Beauty', 'size': 'Medium', 'source': 'Tome of Beasts: 11', 'type': 'Fey' }, { 'alignment': 'unaligned', 'cr': '6', 'name': 'Abominable Sloth', 'size': 'Huge', 'source': 'Primeval Thule Campaign Setting: 220', 'type': 'Beast' },
        { 'alignment': 'chaotic evil', 'cr': '9', 'name': 'Abominable Yeti', 'size': 'Huge', 'source': 'Monster Manual: 306', 'type': 'Monstrosity' }, { 'alignment': 'neutral evil', 'cr': '4', 'name': 'Accursed Defiler', 'size': 'Medium', 'source': 'Tome of Beasts: 12', 'type': 'Undead' }, { 'alignment': 'any', 'cr': '1/4', 'name': 'Acolyte', 'size': 'Medium', 'source': 'Basic Rules v1: 53, HotDQ supplement: 4, Monster Manual: 342', 'type': 'Humanoid' }, { 'alignment': 'lawful evil', 'cr': '2', 'name': 'Adherer', 'size': 'Medium', 'source': 'Fifth Edition Foes: 6', 'type': 'Aberration' }, { 'alignment': 'chaotic evil', 'cr': '14', 'name': 'Adult Black Dragon', 'size': 'Huge', 'source': 'Monster Manual: 88, Princes of the Apocalypse Online Supplement v1.0: 7', 'type': 'Dragon' }, { 'alignment': 'lawful evil', 'cr': '17', 'name': 'Adult Blue Dracolich', 'size': 'Huge', 'source': 'Monster Manual: 84', 'type': 'Undead' }, { 'alignment': 'lawful evil', 'cr': '16', 'name': 'Adult Blue Dragon', 'size': 'Huge', 'source': 'HotDQ supplement: 4, Monster Manual: 91', 'type': 'Dragon' }, { 'alignment': 'chaotic good', 'cr': '13', 'name': 'Adult Brass Dragon', 'size': 'Huge', 'source': 'Monster Manual: 105', 'type': 'Dragon' }, { 'alignment': 'lawful good', 'cr': '15', 'name': 'Adult Bronze Dragon', 'size': 'Huge', 'source': 'Monster Manual: 108, Princes of the Apocalypse Online Supplement v1.0: 7', 'type': 'Dragon' }, { 'alignment': 'neutral evil', 'cr': '16', 'name': 'Adult Cave Dragon', 'size': 'Huge', 'source': 'Tome of Beasts: 125', 'type': 'Dragon' }]

        var actual = findMonsters.monsterFinder();
        expect(actual).toEqual(expected);
    })
})
*/

