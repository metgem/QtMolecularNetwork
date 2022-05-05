#ifndef CONFIG_H
#define CONFIG_H

#ifndef QMN_STATIC
#ifdef QMN_SHARED_EXPORT
#define QMN_EXPORT Q_DECL_EXPORT
#else
#define QMN_EXPORT Q_DECL_IMPORT
#endif
#else
#define QMN_EXPORT
#endif

enum Config: int {
    Radius = 30
};

#endif // CONFIG_H
