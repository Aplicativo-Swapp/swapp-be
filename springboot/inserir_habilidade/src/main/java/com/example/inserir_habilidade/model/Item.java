package com.example.inserir_habilidade.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "usuario_sub_habilidade") // Nome da tabela existente no banco de dados
public class Item {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) // Configuração de auto incremento
    private Long id;

    @Column(name = "id_users", nullable = false) // Mapeia a coluna 'id_users'
    private Long idUsers;

    @Column(name = "id_sub_habilidade", nullable = false) // Mapeia a coluna 'id_sub_habilidade'
    private Long idSubHabilidade;

    @Column(name = "descricao", length = 500) // Mapeia a coluna 'descricao' com limite de 500 caracteres
    private String descricao;

    @Column(name = "valor", nullable = false) // Mapeia a coluna 'valor'
    private Integer valor;

    @Column(name = "created_at", nullable = false) // Mapeia a coluna 'created_at'
    private LocalDateTime createdAt;

    public Item() {}

    public Item(Long idUsers, Long idSubHabilidade, String descricao, Integer valor, LocalDateTime createdAt) {
        this.idUsers = idUsers;
        this.idSubHabilidade = idSubHabilidade;
        this.descricao = descricao;
        this.valor = valor;
        this.createdAt = createdAt;
    }

    // Getters e Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getIdUsers() {
        return idUsers;
    }

    public void setIdUsers(Long idUsers) {
        this.idUsers = idUsers;
    }

    public Long getIdSubHabilidade() {
        return idSubHabilidade;
    }

    public void setIdSubHabilidade(Long idSubHabilidade) {
        this.idSubHabilidade = idSubHabilidade;
    }

    public String getDescricao() {
        return descricao;
    }

    public void setDescricao(String descricao) {
        this.descricao = descricao;
    }

    public Integer getValor() {
        return valor;
    }

    public void setValor(Integer valor) {
        this.valor = valor;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}