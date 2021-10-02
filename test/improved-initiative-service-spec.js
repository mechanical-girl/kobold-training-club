// improved-initiative-service-spec.js
/* jslint node: true */
/* global describe, it, expect */

'use strict';
var iiService = require('../ktc/static/js/improved-initiative-service.js');

describe('generateCombatantPayload', function () {
    it('should create a payload from the provided monsters and monsterData', function () {
        var expected = [
            {
                "Name": "Aalpamac",
                "HP": {
                    "Value": 136
                },
                "TotalInitiativeModifier": 0,
                "AC": {
                    "Value": 16
                },
                "Player": "npc",
                "Id": "tob2.aalpamac"
            },
            {
                "Name": "Aalpamac",
                "HP": {
                    "Value": 136
                },
                "TotalInitiativeModifier": 0,
                "AC": {
                    "Value": 16
                },
                "Player": "npc",
                "Id": "tob2.aalpamac"
            },
            {
                "Name": "Abjurer",
                "HP": {
                    "Value": 84
                },
                "TotalInitiativeModifier": 2,
                "AC": {
                    "Value": 12
                },
                "Player": "npc",
                "Id": "volo.abjurer"
            }
        ]

        var monsters = [
            [
                "Aalpamac",
                2
            ],
            [
                "Abjurer",
                1
            ]
        ]

        var monsterData = [
            [
                "A-mi-kuk",
                "7",
                "Huge",
                "Aberration",
                "",
                "",
                "chaotic evil",
                "Tome of Beasts II: 15",
                "tob2.a-mi-kuk",
                "115",
                "14",
                "-1"
            ],
            [
                "Aalpamac",
                "7",
                "Huge",
                "Monstrosity",
                "",
                "",
                "unaligned",
                "Tome of Beasts II: 8",
                "tob2.aalpamac",
                "136",
                "16",
                "0"
            ],
            [
                "Abjurer",
                "9",
                "Medium",
                "Humanoid",
                "Any Race",
                "NPCs",
                "any alignment",
                "Volo's Guide to Monsters: 209",
                "volo.abjurer",
                "84",
                "12",
                "2"
            ]
        ]

        var actual = iiService.generateCombatantPayload(monsters, monsterData);
        expect(expected).toEqual(actual)
    })
})

describe('openImprovedInitiative', function () {
    it('should open Improved Initiative using the provided payload', function () {
        var payload = {
            Combatants: [
                {
                    "Name": "Aalpamac",
                    "HP": {
                        "Value": 136
                    },
                    "TotalInitiativeModifier": 0,
                    "AC": {
                        "Value": 16
                    },
                    "Player": "npc",
                    "Id": "tob2.aalpamac"
                },
                {
                    "Name": "Aalpamac",
                    "HP": {
                        "Value": 136
                    },
                    "TotalInitiativeModifier": 0,
                    "AC": {
                        "Value": 16
                    },
                    "Player": "npc",
                    "Id": "tob2.aalpamac"
                },
                {
                    "Name": "Abjurer",
                    "HP": {
                        "Value": 84
                    },
                    "TotalInitiativeModifier": 2,
                    "AC": {
                        "Value": 12
                    },
                    "Player": "npc",
                    "Id": "volo.abjurer"
                }
            ]
        };

        var submitted = false;
        var correctUrl = false;
        global.document = {
            createElement: () => {
                return {
                    style: {
                        display: ''
                    },
                    setAttribute: (attrName, attrValue) => {
                        if (attrName == "action") {
                            if (attrValue == "https://www.improved-initiative.com/launchencounter/") {
                                correctUrl = true;
                            }
                        }
                    },
                    appendChild: () => { },
                    submit: () => {
                        submitted = true;
                    },
                    parentNode: {
                        removeChild: () => { }
                    }
                }
            },
            body: {
                appendChild: () => null,
            }
        };
        global.window = {
            document: document
        }

        iiService.openImprovedInitiative(payload);

        expect(submitted).toEqual(true);
        expect(correctUrl).toEqual(true);
    })
})