package com.example.inserir_habilidade.controller;

import com.example.inserir_habilidade.model.Item;
import com.example.inserir_habilidade.repository.ItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;

@RestController
@RequestMapping("/api/habilidades")
public class ItemController {

    @Autowired
    private ItemRepository habilidadeRepository;

    // Insere uma nova habilidade na tabela existente
    @PostMapping
    public ResponseEntity<Object> criarHabilidade(@RequestBody Item habilidade) {
        // Se o campo createdAt não for enviado, ele é setado automaticamente com a data e hora atuais
        if (habilidade.getCreatedAt() == null) {
            habilidade.setCreatedAt(LocalDateTime.now());
        }

        // Salva a nova habilidade no banco de dados
        Item novaHabilidade = habilidadeRepository.save(habilidade);

        // Retorna a resposta com a nova habilidade
        return ResponseEntity.ok(novaHabilidade);
    }
}
