class levels:
  def get(self):
    self.levels=[
      {
        "wall_pos":[],
        "wall_vel":[],
        "enemy_pos":[],
        "enemy_vel":[],
        "enemy_mov":["pacing"],
        "boost_pos":[],
      },
      {
        "wall_pos":[[-200,0],[-100,0],[100,0],[200,0]],
        "wall_vel":[[0,0],[0,0],[0,0],[0,0]],
        "enemy_pos":[[-200,100],[0,100],[200,100]],
        "enemy_vel":[[0,0.2],[0,0.2],[0,0.2]],
        "enemy_mov":["chasing","chasing","chasing"],
        "boost_pos":[[-100,200],[100,200]],
      },
      {
        "wall_pos":[[-200,300],[200,300],[-200,200],[200,200],[-200,100],[200,100],[-200,0],[200,0],[-200,-300],[200,-300],[-200,-200],[200,-200],[-200,-100],[200,-100]],
        "wall_vel":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],
        "enemy_pos":[[-100,100],[100,100]],
        "enemy_vel":[[0.2,0],[-0.2,0]],
        "enemy_mov":["pacing","pacing"],
        "boost_pos":[[-100,0],[0,0],[100,0]]
      }
    ]
    return self.levels
  def test(self):
    print(self.levels)