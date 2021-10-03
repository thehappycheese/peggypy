f={
    "type": "grammar",
    "topLevelInitializer": null,
    "initializer": null,
    "rules": [
       {
          "type": "rule",
          "name": "Expression",
          "nameLocation": {
             "source": undefined,
             "start": {
                "offset": 0,
                "line": 1,
                "column": 1
             },
             "end": {
                "offset": 10,
                "line": 1,
                "column": 11
             }
          },
          "expression": {
             "type": "action",
             "expression": {
                "type": "sequence",
                "elements": [
                   {
                      "type": "labeled",
                      "label": "head",
                      "labelLocation": {
                         "source": undefined,
                         "start": {
                            "offset": 15,
                            "line": 2,
                            "column": 5
                         },
                         "end": {
                            "offset": 19,
                            "line": 2,
                            "column": 9
                         }
                      },
                      "expression": {
                         "type": "rule_ref",
                         "name": "Term",
                         "location": {
                            "source": undefined,
                            "start": {
                               "offset": 20,
                               "line": 2,
                               "column": 10
                            },
                            "end": {
                               "offset": 24,
                               "line": 2,
                               "column": 14
                            }
                         }
                      },
                      "location": {
                         "source": undefined,
                         "start": {
                            "offset": 15,
                            "line": 2,
                            "column": 5
                         },
                         "end": {
                            "offset": 24,
                            "line": 2,
                            "column": 14
                         }
                      }
                   },
                   {
                      "type": "labeled",
                      "label": "tail",
                      "labelLocation": {
                         "source": undefined,
                         "start": {
                            "offset": 25,
                            "line": 2,
                            "column": 15
                         },
                         "end": {
                            "offset": 29,
                            "line": 2,
                            "column": 19
                         }
                      },
                      "expression": {
                         "type": "zero_or_more",
                         "expression": {
                            "type": "group",
                            "expression": {
                               "type": "sequence",
                               "elements": [
                                  {
                                     "type": "rule_ref",
                                     "name": "_",
                                     "location": {
                                        "source": undefined,
                                        "start": {
                                           "offset": 31,
                                           "line": 2,
                                           "column": 21
                                        },
                                        "end": {
                                           "offset": 32,
                                           "line": 2,
                                           "column": 22
                                        }
                                     }
                                  },
                                  {
                                     "type": "choice",
                                     "alternatives": [
                                        {
                                           "type": "literal",
                                           "value": "+",
                                           "ignoreCase": false,
                                           "location": {
                                              "source": undefined,
                                              "start": {
                                                 "offset": 34,
                                                 "line": 2,
                                                 "column": 24
                                              },
                                              "end": {
                                                 "offset": 37,
                                                 "line": 2,
                                                 "column": 27
                                              }
                                           }
                                        },
                                        {
                                           "type": "literal",
                                           "value": "-",
                                           "ignoreCase": false,
                                           "location": {
                                              "source": undefined,
                                              "start": {
                                                 "offset": 40,
                                                 "line": 2,
                                                 "column": 30
                                              },
                                              "end": {
                                                 "offset": 43,
                                                 "line": 2,
                                                 "column": 33
                                              }
                                           }
                                        }
                                     ],
                                     "location": {
                                        "source": undefined,
                                        "start": {
                                           "offset": 34,
                                           "line": 2,
                                           "column": 24
                                        },
                                        "end": {
                                           "offset": 43,
                                           "line": 2,
                                           "column": 33
                                        }
                                     }
                                  },
                                  {
                                     "type": "rule_ref",
                                     "name": "_",
                                     "location": {
                                        "source": undefined,
                                        "start": {
                                           "offset": 45,
                                           "line": 2,
                                           "column": 35
                                        },
                                        "end": {
                                           "offset": 46,
                                           "line": 2,
                                           "column": 36
                                        }
                                     }
                                  },
                                  {
                                     "type": "rule_ref",
                                     "name": "Term",
                                     "location": {
                                        "source": undefined,
                                        "start": {
                                           "offset": 47,
                                           "line": 2,
                                           "column": 37
                                        },
                                        "end": {
                                           "offset": 51,
                                           "line": 2,
                                           "column": 41
                                        }
                                     }
                                  }
                               ],
                               "location": {
                                  "source": undefined,
                                  "start": {
                                     "offset": 31,
                                     "line": 2,
                                     "column": 21
                                  },
                                  "end": {
                                     "offset": 51,
                                     "line": 2,
                                     "column": 41
                                  }
                               }
                            },
                            "location": {
                               "source": undefined,
                               "start": {
                                  "offset": 30,
                                  "line": 2,
                                  "column": 20
                               },
                               "end": {
                                  "offset": 52,
                                  "line": 2,
                                  "column": 42
                               }
                            }
                         },
                         "location": {
                            "source": undefined,
                            "start": {
                               "offset": 30,
                               "line": 2,
                               "column": 20
                            },
                            "end": {
                               "offset": 53,
                               "line": 2,
                               "column": 43
                            }
                         }
                      },
                      "location": {
                         "source": undefined,
                         "start": {
                            "offset": 25,
                            "line": 2,
                            "column": 15
                         },
                         "end": {
                            "offset": 53,
                            "line": 2,
                            "column": 43
                         }
                      }
                   }
                ],
                "location": {
                   "source": undefined,
                   "start": {
                      "offset": 15,
                      "line": 2,
                      "column": 5
                   },
                   "end": {
                      "offset": 53,
                      "line": 2,
                      "column": 43
                   }
                }
             },
             "code": `
       return tail.reduce(function(result, element) {
         if (element[1] === \"+\") { return result + element[3]; }
         if (element[1] === \"-\") { return result - element[3]; }
       }, head);
     `,
             "codeLocation": {
                "source": undefined,
                "start": {
                   "offset": 55,
                   "line": 2,
                   "column": 45
                },
                "end": {
                   "offset": 257,
                   "line": 7,
                   "column": 5
                }
             },
             "location": {
                "source": undefined,
                "start": {
                   "offset": 15,
                   "line": 2,
                   "column": 5
                },
                "end": {
                   "offset": 258,
                   "line": 7,
                   "column": 6
                }
             }
          },
          "location": {
             "source": undefined,
             "start": {
                "offset": 0,
                "line": 1,
                "column": 1
             },
             "end": {
                "offset": 259,
                "line": 8,
                "column": 1
             }
          }
       },
       {
          "type": "rule",
          "name": "Term",
          "nameLocation": {
             "source": undefined,
             "start": {
                "offset": 260,
                "line": 9,
                "column": 1
             },
             "end": {
                "offset": 264,
                "line": 9,
                "column": 5
             }
          },
          "expression": {
             "type": "action",
             "expression": {
                "type": "sequence",
                "elements": [
                   {
                      "type": "labeled",
                      "label": "head",
                      "labelLocation": {
                         "source": undefined,
                         "start": {
                            "offset": 269,
                            "line": 10,
                            "column": 5
                         },
                         "end": {
                            "offset": 273,
                            "line": 10,
                            "column": 9
                         }
                      },
                      "expression": {
                         "type": "rule_ref",
                         "name": "Factor",
                         "location": {
                            "source": undefined,
                            "start": {
                               "offset": 274,
                               "line": 10,
                               "column": 10
                            },
                            "end": {
                               "offset": 280,
                               "line": 10,
                               "column": 16
                            }
                         }
                      },
                      "location": {
                         "source": undefined,
                         "start": {
                            "offset": 269,
                            "line": 10,
                            "column": 5
                         },
                         "end": {
                            "offset": 280,
                            "line": 10,
                            "column": 16
                         }
                      }
                   },
                   {
                      "type": "labeled",
                      "label": "tail",
                      "labelLocation": {
                         "source": undefined,
                         "start": {
                            "offset": 281,
                            "line": 10,
                            "column": 17
                         },
                         "end": {
                            "offset": 285,
                            "line": 10,
                            "column": 21
                         }
                      },
                      "expression": {
                         "type": "zero_or_more",
                         "expression": {
                            "type": "group",
                            "expression": {
                               "type": "sequence",
                               "elements": [
                                  {
                                     "type": "rule_ref",
                                     "name": "_",
                                     "location": {
                                        "source": undefined,
                                        "start": {
                                           "offset": 287,
                                           "line": 10,
                                           "column": 23
                                        },
                                        "end": {
                                           "offset": 288,
                                           "line": 10,
                                           "column": 24
                                        }
                                     }
                                  },
                                  {
                                     "type": "choice",
                                     "alternatives": [
                                        {
                                           "type": "literal",
                                           "value": "*",
                                           "ignoreCase": false,
                                           "location": {
                                              "source": undefined,
                                              "start": {
                                                 "offset": 290,
                                                 "line": 10,
                                                 "column": 26
                                              },
                                              "end": {
                                                 "offset": 293,
                                                 "line": 10,
                                                 "column": 29
                                              }
                                           }
                                        },
                                        {
                                           "type": "literal",
                                           "value": "/",
                                           "ignoreCase": false,
                                           "location": {
                                              "source": undefined,
                                              "start": {
                                                 "offset": 296,
                                                 "line": 10,
                                                 "column": 32
                                              },
                                              "end": {
                                                 "offset": 299,
                                                 "line": 10,
                                                 "column": 35
                                              }
                                           }
                                        }
                                     ],
                                     "location": {
                                        "source": undefined,
                                        "start": {
                                           "offset": 290,
                                           "line": 10,
                                           "column": 26
                                        },
                                        "end": {
                                           "offset": 299,
                                           "line": 10,
                                           "column": 35
                                        }
                                     }
                                  },
                                  {
                                     "type": "rule_ref",
                                     "name": "_",
                                     "location": {
                                        "source": undefined,
                                        "start": {
                                           "offset": 301,
                                           "line": 10,
                                           "column": 37
                                        },
                                        "end": {
                                           "offset": 302,
                                           "line": 10,
                                           "column": 38
                                        }
                                     }
                                  },
                                  {
                                     "type": "rule_ref",
                                     "name": "Factor",
                                     "location": {
                                        "source": undefined,
                                        "start": {
                                           "offset": 303,
                                           "line": 10,
                                           "column": 39
                                        },
                                        "end": {
                                           "offset": 309,
                                           "line": 10,
                                           "column": 45
                                        }
                                     }
                                  }
                               ],
                               "location": {
                                  "source": undefined,
                                  "start": {
                                     "offset": 287,
                                     "line": 10,
                                     "column": 23
                                  },
                                  "end": {
                                     "offset": 309,
                                     "line": 10,
                                     "column": 45
                                  }
                               }
                            },
                            "location": {
                               "source": undefined,
                               "start": {
                                  "offset": 286,
                                  "line": 10,
                                  "column": 22
                               },
                               "end": {
                                  "offset": 310,
                                  "line": 10,
                                  "column": 46
                               }
                            }
                         },
                         "location": {
                            "source": undefined,
                            "start": {
                               "offset": 286,
                               "line": 10,
                               "column": 22
                            },
                            "end": {
                               "offset": 311,
                               "line": 10,
                               "column": 47
                            }
                         }
                      },
                      "location": {
                         "source": undefined,
                         "start": {
                            "offset": 281,
                            "line": 10,
                            "column": 17
                         },
                         "end": {
                            "offset": 311,
                            "line": 10,
                            "column": 47
                         }
                      }
                   }
                ],
                "location": {
                   "source": undefined,
                   "start": {
                      "offset": 269,
                      "line": 10,
                      "column": 5
                   },
                   "end": {
                      "offset": 311,
                      "line": 10,
                      "column": 47
                   }
                }
             },
             "code": `
       return tail.reduce(function(result, element) {
         if (element[1] === \"*\") { return result * element[3]; }
         if (element[1] === \"/\") { return result / element[3]; }
       }, head);
     `,
             "codeLocation": {
                "source": undefined,
                "start": {
                   "offset": 313,
                   "line": 10,
                   "column": 49
                },
                "end": {
                   "offset": 515,
                   "line": 15,
                   "column": 5
                }
             },
             "location": {
                "source": undefined,
                "start": {
                   "offset": 269,
                   "line": 10,
                   "column": 5
                },
                "end": {
                   "offset": 516,
                   "line": 15,
                   "column": 6
                }
             }
          },
          "location": {
             "source": undefined,
             "start": {
                "offset": 260,
                "line": 9,
                "column": 1
             },
             "end": {
                "offset": 517,
                "line": 16,
                "column": 1
             }
          }
       },
       {
          "type": "rule",
          "name": "Factor",
          "nameLocation": {
             "source": undefined,
             "start": {
                "offset": 518,
                "line": 17,
                "column": 1
             },
             "end": {
                "offset": 524,
                "line": 17,
                "column": 7
             }
          },
          "expression": {
             "type": "choice",
             "alternatives": [
                {
                   "type": "action",
                   "expression": {
                      "type": "sequence",
                      "elements": [
                         {
                            "type": "literal",
                            "value": "(",
                            "ignoreCase": false,
                            "location": {
                               "source": undefined,
                               "start": {
                                  "offset": 529,
                                  "line": 18,
                                  "column": 5
                               },
                               "end": {
                                  "offset": 532,
                                  "line": 18,
                                  "column": 8
                               }
                            }
                         },
                         {
                            "type": "rule_ref",
                            "name": "_",
                            "location": {
                               "source": undefined,
                               "start": {
                                  "offset": 533,
                                  "line": 18,
                                  "column": 9
                               },
                               "end": {
                                  "offset": 534,
                                  "line": 18,
                                  "column": 10
                               }
                            }
                         },
                         {
                            "type": "labeled",
                            "label": "expr",
                            "labelLocation": {
                               "source": undefined,
                               "start": {
                                  "offset": 535,
                                  "line": 18,
                                  "column": 11
                               },
                               "end": {
                                  "offset": 539,
                                  "line": 18,
                                  "column": 15
                               }
                            },
                            "expression": {
                               "type": "rule_ref",
                               "name": "Expression",
                               "location": {
                                  "source": undefined,
                                  "start": {
                                     "offset": 540,
                                     "line": 18,
                                     "column": 16
                                  },
                                  "end": {
                                     "offset": 550,
                                     "line": 18,
                                     "column": 26
                                  }
                               }
                            },
                            "location": {
                               "source": undefined,
                               "start": {
                                  "offset": 535,
                                  "line": 18,
                                  "column": 11
                               },
                               "end": {
                                  "offset": 550,
                                  "line": 18,
                                  "column": 26
                               }
                            }
                         },
                         {
                            "type": "rule_ref",
                            "name": "_",
                            "location": {
                               "source": undefined,
                               "start": {
                                  "offset": 551,
                                  "line": 18,
                                  "column": 27
                               },
                               "end": {
                                  "offset": 552,
                                  "line": 18,
                                  "column": 28
                               }
                            }
                         },
                         {
                            "type": "literal",
                            "value": ")",
                            "ignoreCase": false,
                            "location": {
                               "source": undefined,
                               "start": {
                                  "offset": 553,
                                  "line": 18,
                                  "column": 29
                               },
                               "end": {
                                  "offset": 556,
                                  "line": 18,
                                  "column": 32
                               }
                            }
                         }
                      ],
                      "location": {
                         "source": undefined,
                         "start": {
                            "offset": 529,
                            "line": 18,
                            "column": 5
                         },
                         "end": {
                            "offset": 556,
                            "line": 18,
                            "column": 32
                         }
                      }
                   },
                   "code": ` return expr; `,
                   "codeLocation": {
                      "source": undefined,
                      "start": {
                         "offset": 558,
                         "line": 18,
                         "column": 34
                      },
                      "end": {
                         "offset": 572,
                         "line": 18,
                         "column": 48
                      }
                   },
                   "location": {
                      "source": undefined,
                      "start": {
                         "offset": 529,
                         "line": 18,
                         "column": 5
                      },
                      "end": {
                         "offset": 573,
                         "line": 18,
                         "column": 49
                      }
                   }
                },
                {
                   "type": "rule_ref",
                   "name": "Integer",
                   "location": {
                      "source": undefined,
                      "start": {
                         "offset": 578,
                         "line": 19,
                         "column": 5
                      },
                      "end": {
                         "offset": 585,
                         "line": 19,
                         "column": 12
                      }
                   }
                }
             ],
             "location": {
                "source": undefined,
                "start": {
                   "offset": 529,
                   "line": 18,
                   "column": 5
                },
                "end": {
                   "offset": 585,
                   "line": 19,
                   "column": 12
                }
             }
          },
          "location": {
             "source": undefined,
             "start": {
                "offset": 518,
                "line": 17,
                "column": 1
             },
             "end": {
                "offset": 586,
                "line": 20,
                "column": 1
             }
          }
       },
       {
          "type": "rule",
          "name": "Integer",
          "nameLocation": {
             "source": undefined,
             "start": {
                "offset": 587,
                "line": 21,
                "column": 1
             },
             "end": {
                "offset": 594,
                "line": 21,
                "column": 8
             }
          },
          "expression": {
             "type": "named",
             "name": "integer",
             "expression": {
                "type": "action",
                "expression": {
                   "type": "sequence",
                   "elements": [
                      {
                         "type": "rule_ref",
                         "name": "_",
                         "location": {
                            "source": undefined,
                            "start": {
                               "offset": 609,
                               "line": 22,
                               "column": 5
                            },
                            "end": {
                               "offset": 610,
                               "line": 22,
                               "column": 6
                            }
                         }
                      },
                      {
                         "type": "one_or_more",
                         "expression": {
                            "type": "class",
                            "parts": [
                               [
                                  "0",
                                  "9"
                               ]
                            ],
                            "inverted": false,
                            "ignoreCase": false,
                            "location": {
                               "source": undefined,
                               "start": {
                                  "offset": 611,
                                  "line": 22,
                                  "column": 7
                               },
                               "end": {
                                  "offset": 616,
                                  "line": 22,
                                  "column": 12
                               }
                            }
                         },
                         "location": {
                            "source": undefined,
                            "start": {
                               "offset": 611,
                               "line": 22,
                               "column": 7
                            },
                            "end": {
                               "offset": 617,
                               "line": 22,
                               "column": 13
                            }
                         }
                      }
                   ],
                   "location": {
                      "source": undefined,
                      "start": {
                         "offset": 609,
                         "line": 22,
                         "column": 5
                      },
                      "end": {
                         "offset": 617,
                         "line": 22,
                         "column": 13
                      }
                   }
                },
                "code": ` return parseInt(text(), 10); `,
                "codeLocation": {
                   "source": undefined,
                   "start": {
                      "offset": 619,
                      "line": 22,
                      "column": 15
                   },
                   "end": {
                      "offset": 649,
                      "line": 22,
                      "column": 45
                   }
                },
                "location": {
                   "source": undefined,
                   "start": {
                      "offset": 609,
                      "line": 22,
                      "column": 5
                   },
                   "end": {
                      "offset": 650,
                      "line": 22,
                      "column": 46
                   }
                }
             },
             "location": {
                "source": undefined,
                "start": {
                   "offset": 587,
                   "line": 21,
                   "column": 1
                },
                "end": {
                   "offset": 651,
                   "line": 23,
                   "column": 1
                }
             }
          },
          "location": {
             "source": undefined,
             "start": {
                "offset": 587,
                "line": 21,
                "column": 1
             },
             "end": {
                "offset": 651,
                "line": 23,
                "column": 1
             }
          }
       },
       {
          "type": "rule",
          "name": "_",
          "nameLocation": {
             "source": undefined,
             "start": {
                "offset": 652,
                "line": 24,
                "column": 1
             },
             "end": {
                "offset": 653,
                "line": 24,
                "column": 2
             }
          },
          "expression": {
             "type": "named",
             "name": "whitespace",
             "expression": {
                "type": "zero_or_more",
                "expression": {
                   "type": "class",
                   "parts": [
                      " ",
                      "	",
                      "
 ",
                      "
 "
                   ],
                   "inverted": false,
                   "ignoreCase": false,
                   "location": {
                      "source": undefined,
                      "start": {
                         "offset": 671,
                         "line": 25,
                         "column": 5
                      },
                      "end": {
                         "offset": 680,
                         "line": 25,
                         "column": 14
                      }
                   }
                },
                "location": {
                   "source": undefined,
                   "start": {
                      "offset": 671,
                      "line": 25,
                      "column": 5
                   },
                   "end": {
                      "offset": 681,
                      "line": 25,
                      "column": 15
                   }
                }
             },
             "location": {
                "source": undefined,
                "start": {
                   "offset": 652,
                   "line": 24,
                   "column": 1
                },
                "end": {
                   "offset": 681,
                   "line": 25,
                   "column": 15
                }
             }
          },
          "location": {
             "source": undefined,
             "start": {
                "offset": 652,
                "line": 24,
                "column": 1
             },
             "end": {
                "offset": 681,
                "line": 25,
                "column": 15
             }
          }
       }
    ],
    "location": {
       "source": undefined,
       "start": {
          "offset": 0,
          "line": 1,
          "column": 1
       },
       "end": {
          "offset": 681,
          "line": 25,
          "column": 15
       }
    }
 }