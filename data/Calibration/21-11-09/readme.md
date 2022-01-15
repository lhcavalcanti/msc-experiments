## Caminhos a serem percorridos:
- Square (S)
  - X [-2, 0, 0, -2]
  - Y [-1, -1, 1, 1]
- Line(L)
  - X [-2, 0.2]
  - Y [-1, -1]
- Zigzag(Z)
  - X [-2, 0.2]
  - Y [-1, -1]

### Navegação por Visão:
1. Teste: (L, S, Z) 
    Positoin: Move | Log: Speed
        L: RMSE: 0.2782712533039086
        S: RMSE: 0.2254544441145846

2. Teste: (L, S, Z)
    Positoin: Speed | Log: Speed
        L : RMSE: 0.2810929883564871
        S: RMSE: 0.23139502139308507

3. Teste: (L, S, Z)
    Positoin: Move | Log: Move

### Navegação Embarcada (sem update):
4. Teste: (L, L, L)   <- Samples to train!
    Positoin: Move | **Log: Speed**
        L: RMSE: 0.23588851134544978
        L: RMSE: 0.25498702739997114
        L: RMSE: 0.23482425158433345

5. Teste: (L, L, L)   <- Samples to train!
    Positoin: Speed | **Log: Speed**
        L: RMSE: 0.19855229267640642 (bad samples)
        L: RMSE: 0.259342207574748
        L: RMSE: 0.25217154676612824
        L: RMSE: 0.26093837670024495

6. Teste: (L, L, L) 
    Positoin: Move | Log: Move

### Navegação Embarcada (10 fps)
7. Teste: (L, S, Z)
    Positoin: Move | Log: Speed
8. Teste: (L, S, Z)
    Positoin: Speed | Log: Speed
        L: RMSE: 0.016655156997450127
        S: RMSE: 0.01740119769954551

9. Teste: (L, S, Z)
    Positoin: Move | Log: Move
