class DataLoader():
    def load():
        DataLoader.load_hero_defaults()

    def load_hero_defaults():
        import GameEngine.HeroDefinition as hero_def
        import GameEngine.Action as actions

        hero_def.Thief.default_actions = [actions.Stealth]