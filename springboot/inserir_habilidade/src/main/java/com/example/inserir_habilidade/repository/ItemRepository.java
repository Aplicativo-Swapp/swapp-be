package com.example.inserir_habilidade.repository;

import com.example.inserir_habilidade.model.Item;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ItemRepository extends JpaRepository<Item, Long> {
}
